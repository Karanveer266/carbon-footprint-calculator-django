from django.urls import path
from . import views

urlpatterns = [
    path('', views.calculator_home, name='calculator_home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('transportation/', views.transportation_step, name='transportation_step'),
    path('food-diet/', views.food_diet_step, name='food_diet_step'),
    path('home-energy/', views.home_energy_step, name='home_energy_step'),
    path('consumer-goods/', views.consumer_goods_step, name='consumer_goods_step'),
    path('results/', views.results_step, name='results_step'),
    path('reset/', views.reset_calculator, name='reset_calculator'),
    path('footprint/<int:record_id>/', views.footprint_detail, name='footprint_detail'),
]