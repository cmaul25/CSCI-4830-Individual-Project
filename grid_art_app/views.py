from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def grid(request):
    return render(request, 'grid.html')