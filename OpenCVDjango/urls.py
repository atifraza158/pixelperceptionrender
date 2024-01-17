from django.contrib import admin
from django.urls import path, include
from image_processing.views import *

urlpatterns = [
    # path('', home, name='home'),    
    path('', include('image_processing.urls')),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
