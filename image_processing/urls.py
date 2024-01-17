from django.urls import path, include
from image_processing.views import *

urlpatterns = [
    path('', main, name='main'),
    path('convert_rgb_to_gray/', convert_rgb_to_gray, name='gray-conversion'),
    path('blur_image/', blur_image, name='blur-image'),
    path('edge_detection/', edge_detection, name='edge-detection'),
    path('compress_image/', compress_image, name='compress-image'),
    path('convert_png_to_jpg/', convert_png_image, name='convert-png-to-jpg'),
    path('resize_image/', resize_image, name='resize-image'),
    path('convert_webpg_to_jpg/', convert_webp_to_jpg, name='convert-webp-to-jpg'),
    path('convert_jpg_to_webp/', convert_jpg_to_webp, name='convert-jpg-to-webp'),
    # path('success/', success, name='success'),
]
