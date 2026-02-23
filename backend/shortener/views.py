from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import URL

@api_view(['POST'])
def shorten_url(request):
    """Takes a long URL and returns the short code."""
    long_url = request.data.get('long_url')
    # Get existing if already shortened, or create new
    url_obj, created = URL.objects.get_or_create(long_url=long_url)
    
    return Response({
        'short_code': url_obj.short_code,
        'long_url': url_obj.long_url,
        'short_url': f"http://localhost:8000/{url_obj.short_code}"
    })

def redirect_view(request, short_code):
    url_obj = get_object_or_404(URL, short_code=short_code)
    url_obj.clicks += 1  # Increment the click count
    url_obj.save()
    return redirect(url_obj.long_url)

# Add a new view to fetch all links for the dashboard
@api_view(['GET'])
def get_all_urls(request):
    urls = URL.objects.all().order_by('-created_at')
    data = [{
        "id": u.id,  # Important for later!
        "short_url": f"http://localhost:8000/{u.short_code}",
        "long_url": u.long_url,
        "clicks": u.clicks,
        "created_at": u.created_at.strftime("%Y-%m-%d")
    } for u in urls]
    return Response(data)