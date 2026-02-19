from django.urls import path 
from grid_art_app import views 
#urls patterns
urlpatterns = [ path('', views.home, name='home'), 
path('gird/', views.grid, name='grid'), 
]