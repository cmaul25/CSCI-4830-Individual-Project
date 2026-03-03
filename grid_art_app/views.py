from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Pixel
from django.contrib.auth.models import User
import json

def home(request):
    return render(request, 'home.html')

def grid(request):
    width = 250
    height = 200
    changed_pixels = Pixel.objects.all()
    pixel_dict = {(p.x, p.y): p.color for p in changed_pixels}
    grid = []
    for y in range(height):
        row = []
        for x in range(width):
            color = pixel_dict.get((x, y), '#FFFFFF')
            row.append({'x': x, 'y': y, 'color': color})
        grid.append(row)
    return render(request, 'grid.html', {'grid': grid})

@csrf_exempt
def update_pixel(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        x = int(data['x'])
        y = int(data['y'])
        color = data['color']
        signature = data['signature']

        pixel, created = Pixel.objects.update_or_create(
            x=x, y=y,
            defaults={'color': color, 'changed_by': signature}
        )
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})