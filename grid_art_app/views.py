from django.shortcuts import render
from .models import Pixel

def home(request):
    return render(request, 'home.html')

def grid(request):
    width = 250
    height = 200
    
    # Get all pixels that have been changed from the database
    changed_pixels = Pixel.objects.all()
    pixel_dict = {(p.x, p.y): p.color for p in changed_pixels}
    
    # Build the grid
    grid = []
    for y in range(height):
        row = []
        for x in range(width):
            color = pixel_dict.get((x, y), '#FFFFFF')  # default white
            row.append({'x': x, 'y': y, 'color': color})
        grid.append(row)
    
    return render(request, 'grid.html', {'grid': grid})