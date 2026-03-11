from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Pixel
from django.contrib.auth.models import User
import json
from django.db.models import Count, Min

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
        # Most pixels
    most_pixels = (Pixel.objects
        .values('changed_by')
        .annotate(count=Count('id'))
        .order_by('-count')[:10])

    # Most colors used
    most_colors = (Pixel.objects
        .values('changed_by')
        .annotate(count=Count('color', distinct=True))
        .order_by('-count')[:10])

    # Oldest pixel (user whose oldest pixel is the oldest)
    oldest_pixels = (Pixel.objects
        .values('changed_by')
        .annotate(oldest=Min('timestamp'))
        .order_by('oldest')[:10])

    return render(request, 'grid.html', {
        'pixel_data': pixel_data,
        'most_pixels': most_pixels,
        'most_colors': most_colors,
        'oldest_pixels': oldest_pixels,
        })

def get_leaderboard(request):
    most_pixels = list(Pixel.objects
        .values('changed_by')
        .annotate(count=Count('id'))
        .order_by('-count')[:10])

    most_colors = list(Pixel.objects
        .values('changed_by')
        .annotate(count=Count('color', distinct=True))
        .order_by('-count')[:10])

    oldest_pixels = list(Pixel.objects
        .values('changed_by')
        .annotate(oldest=Min('timestamp'))
        .order_by('oldest')[:10])

    # Convert timestamps to strings so they are JSON serializable
    for entry in oldest_pixels:
        entry['oldest'] = entry['oldest'].strftime('%m/%d/%Y') if entry['oldest'] else '-'

    return JsonResponse({
        'most_pixels': most_pixels,
        'most_colors': most_colors,
        'oldest_pixels': oldest_pixels,
    })

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