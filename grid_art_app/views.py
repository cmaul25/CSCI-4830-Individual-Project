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
    pixel_info = {(p.x, p.y): {'changed_by': p.changed_by, 'timestamp': p.timestamp.strftime('%Y-%m-%d %H:%M:%S') if p.timestamp else '-'} for p in changed_pixels}
    grid = []
    for y in range(height):
        row = []
        for x in range(width):
            color = pixel_dict.get((x, y), '#FFFFFF')
            info = pixel_info.get((x, y), {'changed_by': 'Unchanged', 'timestamp': '-'})
            row.append({'x': x, 'y': y, 'color': color, 'changed_by': info['changed_by'], 'timestamp': info['timestamp']})
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