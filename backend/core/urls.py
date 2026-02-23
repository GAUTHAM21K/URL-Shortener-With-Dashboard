"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings
from shortener.views import shorten_url, redirect_view, get_all_urls
import os
from django.http import FileResponse, HttpResponse

def serve_react(request, path=None):
    """Serve React app for SPA routing."""
    # Try to serve the index.html from static files
    from django.conf import settings
    index_path = os.path.join(settings.STATIC_ROOT, 'index.html')
    if os.path.exists(index_path):
        try:
            return FileResponse(open(index_path, 'rb'), content_type='text/html')
        except Exception:
            return HttpResponse('Frontend not available', status=404)
    return HttpResponse('Frontend not available', status=404)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API Endpoints (must come BEFORE catch-all)
    path('api/shorten/', shorten_url),   # POST: Create link
    path('api/urls/', get_all_urls),     # GET: Fetch all links
    
    # Static files serving
    re_path(r'^static/(?P<path>.*)$', serve, 
            {'document_root': settings.STATIC_ROOT}),
    
    # Redirect Path (short codes)
    path('<str:short_code>/', redirect_view),
    
    # Catch-all for SPA routing (MUST BE LAST)
    re_path(r'^(?P<path>.*)$', serve_react),
]