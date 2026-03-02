from django.urls import path
from . import views
#url patterns grid is the home page
urlpatterns = [
    path('', views.grid, name='grid'),
    path('update_pixel/', views.update_pixel, name='update_pixel'),
]