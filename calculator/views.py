import os
import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from .forms import TransportationForm, FoodDietForm, HomeEnergyForm, ConsumerGoodsForm, FoodInvoiceForm
from .models import FootprintRecord
from .utils import analyze_with_gemma, analyze_food_invoice, encode_image, extract_footprint_values

@login_required
def dashboard(request):
    """User dashboard showing footprint history"""
    footprint_records = FootprintRecord.objects.filter(user=request.user).order_by('-date')
    
    # Prepare data for the chart
    dates = [record.date.strftime('%Y-%m-%d') for record in footprint_records]
    footprints = [record.total_footprint for record in footprint_records]
    
    context = {
        'footprint_records': footprint_records,
        'chart_dates': json.dumps(dates),
        'chart_footprints': json.dumps(footprints),
    }
    return render(request, 'calculator/dashboard.html', context)

@login_required
def calculator_home(request):
    """Starting page for the calculator"""
    return render(request, 'calculator/home.html')

@login_required
def transportation_step(request):
    """Step 1: Transportation"""
    # Initialize or get session data
    if 'user_responses' not in request.session:
        request.session['user_responses'] = {}
        request.session['results_processing'] = False
    
    if request.method == 'POST':
        form = TransportationForm(request.POST)
        if form.is_valid():
            # Store form data in session
            request.session['user_responses']['transportation'] = form.cleaned_data
            request.session.modified = True
            return redirect('food_diet_step')
    else:
        # Pre-fill form with session data if available
        initial_data = request.session.get('user_responses', {}).get('transportation', {})
        form = TransportationForm(initial=initial_data)
    
    return render(request, 'calculator/transportation.html', {'form': form})

@login_required
def food_diet_step(request):
    """Step 2: Food & Diet"""
    if request.method == 'POST':
        form = FoodDietForm(request.POST)
        if form.is_valid():
            # Store form data in session
            request.session['user_responses']['food'] = form.cleaned_data
            request.session.modified = True
            return redirect('home_energy_step')
    else:
        # Pre-fill form with session data if available
        initial_data = request.session.get('user_responses', {}).get('food', {})
        form = FoodDietForm(initial=initial_data)
    
    return render(request, 'calculator/food_diet.html', {'form': form})

@login_required
def home_energy_step(request):
    """Step 3: Home Energy"""
    if request.method == 'POST':
        form = HomeEnergyForm(request.POST)
        if form.is_valid():
            # Store form data in session
            request.session['user_responses']['home_energy'] = form.cleaned_data
            request.session.modified = True
            return redirect('consumer_goods_step')
    else:
        # Pre-fill form with session data if available
        initial_data = request.session.get('user_responses', {}).get('home_energy', {})
        form = HomeEnergyForm(initial=initial_data)
    
    return render(request, 'calculator/home_energy.html', {'form': form})

@login_required
def consumer_goods_step(request):
    """Step 4: Consumer Goods"""
    if request.method == 'POST':
        form = ConsumerGoodsForm(request.POST)
        if form.is_valid():
            # Store form data in session
            request.session['user_responses']['consumer_goods'] = form.cleaned_data
            request.session.modified = True
            
            # Set processing flag to False initially
            request.session['results_processing'] = False
            request.session.modified = True
            
            # Redirect to loading page instead of results
            return redirect('loading_page')
    else:
        # Pre-fill form with session data if available
        initial_data = request.session.get('user_responses', {}).get('consumer_goods', {})
        form = ConsumerGoodsForm(initial=initial_data)
    
    return render(request, 'calculator/consumer_goods.html', {'form': form})

@login_required
def loading_page(request):
    """Loading page while waiting for results"""
    # If results are already available, redirect to results page
    if 'final_result' in request.session:
        return redirect('view_results')
    
    # If processing hasn't started yet, set the flag
    if not request.session.get('results_processing', False):
        request.session['results_processing'] = True
        request.session.modified = True
    
    return render(request, 'calculator/loading.html')

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@login_required
def process_results(request):
    """Process the results in the background"""
    # This view should be called via AJAX or redirect from the loading page
    # It should not be accessed directly by the user
    
    # Calculate the carbon footprint
    user_responses = request.session.get('user_responses', {})
    
    # Get the analysis from Gemma
    analysis = analyze_with_gemma(user_responses)
    request.session['final_result'] = analysis
    
    # Extract numerical values from the analysis
    footprint_values = extract_footprint_values(analysis)
    
    # Save the record to the database
    FootprintRecord.objects.create(
        user=request.user,
        total_footprint=footprint_values['total'],
        transportation_footprint=footprint_values['transportation'],
        food_footprint=footprint_values['food'],
        home_energy_footprint=footprint_values['home_energy'],
        consumption_footprint=footprint_values['consumption'],
        detailed_analysis=analysis,
        raw_responses=user_responses
    )
    
    # Set processing flag to False
    request.session['results_processing'] = False
    request.session.modified = True
    
    return JsonResponse({'status': 'processing_complete'})

@login_required
def check_results_status(request):
    """Check if results are ready"""
    # This view is called via AJAX from the loading page
    ready = 'final_result' in request.session and not request.session.get('results_processing', False)
    
    return JsonResponse({'ready': ready})

@login_required
def view_results(request):
    """View the results"""
    # If results are not available, redirect to the loading page
    if 'final_result' not in request.session:
        return redirect('loading_page')
    
    context = {
        'analysis': request.session.get('final_result', ''),
    }
    return render(request, 'calculator/results.html', context)

@login_required
def reset_calculator(request):
    """Reset the calculator session data"""
    if 'user_responses' in request.session:
        del request.session['user_responses']
    if 'final_result' in request.session:
        del request.session['final_result']
    
    messages.success(request, "Calculator has been reset. You can start a new calculation.")
    return redirect('calculator_home')

@login_required
def footprint_detail(request, record_id):
    """View detailed analysis for a specific footprint record"""
    try:
        record = FootprintRecord.objects.get(id=record_id, user=request.user)
        context = {'record': record}
        return render(request, 'calculator/footprint_detail.html', context)
    except FootprintRecord.DoesNotExist:
        messages.error(request, "Record not found.")
