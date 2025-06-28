from django.urls import path
from . import views

urlpatterns = [
    path('', views.calculator_home, name='calculator_home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('transportation/', views.transportation_step, name='transportation_step'),
    path('food-diet/', views.food_diet_step, name='food_diet_step'),
    path('home-energy/', views.home_energy_step, name='home_energy_step'),
    path('consumer-goods/', views.consumer_goods_step, name='consumer_goods_step'),
    path('loading/', views.loading_page, name='loading_page'),
    path('check-results/', views.check_results_status, name='check_results_status'),
    path('results/', views.view_results, name='view_results'),
    path('process-results/', views.process_results, name='process_results'),
    path('reset/', views.reset_calculator, name='reset_calculator'),
    path('footprint/<int:record_id>/', views.footprint_detail, name='footprint_detail'),
]