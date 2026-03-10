from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Pixel
from django.contrib.auth.models import User
import json

def grid(request):
    changed_pixels = Pixel.objects.all().values('x', 'y', 'color', 'changed_by', 'timestamp')
    pixel_data = []
    for p in changed_pixels:
        pixel_data.append({
            'x': p['x'],
            'y': p['y'],
            'color': p['color'],
            'changed_by': p['changed_by'] or 'Unknown',
            'timestamp': p['timestamp'].strftime('%Y-%m-%d %H:%M:%S') if p['timestamp'] else '-'
        })
    return render(request, 'grid.html', {'pixel_data': pixel_data})

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