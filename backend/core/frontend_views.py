from django.views.static import serve
from django.conf import settings
from django.http import FileResponse
from pathlib import Path
import os

def serve_frontend(request):
    """Serve React frontend for SPA routing."""
    # Try to serve static files from the dist folder if they exist
    index_path = os.path.join(settings.STATIC_ROOT, 'index.html')
    
    # If index.html exists in static files (built frontend), serve it
    if os.path.exists(index_path):
        return FileResponse(open(index_path, 'rb'), content_type='text/html')
    
    # Otherwise return 404
    from django.http import HttpResponse
    return HttpResponse('Not found', status=404)
