# import base64
import base64
import os
import tempfile
import cv2
from django.shortcuts import redirect, render
from django.contrib.sessions.models import Session
from django.conf import settings
from django.contrib import messages
import shutil
from django.core.cache import cache
import numpy as np
# from PIL import Image
# import numpy as np
# from rembg import remove 


def main(request):
    context = {
        'title' : "Home Page",
    }
    return render(request, 'main.html', context=context)

# ------------------------- Converting RGB images to GRAY images ------------------------

# def convert_rgb_to_gray(request):  
#     # Getting image as input from the user 
#     if request.method == 'POST':
#         image_file = request.FILES.get('image')
#         img = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)
        
#         # Convert to grayscale
#         gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#         # Save the original and processed images to cache for a very short time
#         cache.set('original_image', img, 600)
#         cache.set('processed_image', gray_image, 600) # 600 seconds (10 minutes)
        
#         return redirect('success')
        
#     return render(request, 'convert_gray.html')

# def convert_image_to_base64(image):
#     _, buffer = cv2.imencode('.jpg', image)
#     image_encoded = base64.b64encode(buffer).decode('utf-8')
#     return f'data:image/jpeg;base64,{image_encoded}'

# def success(request):
#     original_image = cache.get('original_image')
#     processed_image = cache.get('processed_image')

#     if original_image is None or processed_image is None:
#         messages.error(request, "Images not found in cache.")
#         return redirect('blur_image')

#     # Convert images to base64-encoded strings
#     original_image_base64 = convert_image_to_base64(original_image)
#     processed_image_base64 = convert_image_to_base64(processed_image)

#     context = {
#         'original_image_path': original_image_base64,
#         'processed_image_path': processed_image_base64,
#     }

#     return render(request, 'success.html', context=context)


# Old Technique of Local Folders
def convert_rgb_to_gray(request):
    
    uploaded_images_path = 'media/uploaded_images/'
    processed_images_path = 'media/processed_images/'
    
    empty_directories(uploaded_images_path, processed_images_path)
    
    
    original_image_path = ''
    # Getting image as input from the user 
    if request.method == 'POST':
        image_path = 'media/uploaded_images/'
        os.makedirs(image_path, exist_ok=True)
        
        image_file = request.FILES.get('image')
        image_path = os.path.join(image_path, image_file.name)
        
        with open(image_path, 'wb') as destination:
            for chunk in image_file.chunks():
                destination.write(chunk)
                
        img = cv2.imread(image_path)
        
        if img is None:
            messages.error(request, "Image Not Found")
            return redirect('blur_image')
        
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # cv2.imshow("Gray Image", gray_image)
        # cv2.waitKey(0)
        
        output_path = os.path.join(settings.BASE_DIR, f'media/processed_images/{image_file.name}')
        cv2.imwrite(output_path, gray_image)
        
        request.session['original_image_path'] = original_image_path
        original_image_path = f'/media/uploaded_images/{image_file.name}'
        processed_image_path = f'/media/processed_images/{image_file.name}'
        context = {
            'processed_image_path' : processed_image_path,
            'original_image_path' : original_image_path,
        }
        print(processed_image_path)
        return render(request, "success.html", context=context)
        
    return render(request, 'convert_gray.html')


# -------------------------- View for Image Blurring -----------------------------
def blur_image(request):
    uploaded_images_path = 'media/uploaded_images/'
    processed_images_path = 'media/processed_images/'
    
    empty_directories(uploaded_images_path, processed_images_path)
    original_image_path = ''
    try:
        if request.method == 'POST':
            blur_intensity = int(request.POST.get('blur_intensity'))
            image_path = "media/uploaded_images/"
            os.makedirs(image_path, exist_ok=True)
            
            image_file = request.FILES.get('image')
            image_path = os.path.join(image_path, image_file.name)
            
            with open(image_path, 'wb') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)
                    
            img = cv2.imread(image_path)
            
            blurred_image = cv2.GaussianBlur(img, (blur_intensity, blur_intensity), 0)
            
            output_path = os.path.join(settings.BASE_DIR, f'media/processed_images/{image_file.name}')
            cv2.imwrite(output_path, blurred_image)
            
            request.session['original_image_path'] = original_image_path
            original_image_path = f'/media/uploaded_images/{image_file.name}'
            processed_image_path = f'/media/processed_images/{image_file.name}'
            context = {
                'processed_image_path' : processed_image_path,
                'original_image_path' : original_image_path,
            }
            
            return render(request, 'success.html', context=context)
    except Exception as e:
        messages.error(request, "Something went wrong")
                        
    return render(request, 'blur_image.html')


# ------------------ Edge Detection --------------------------------
def edge_detection(request):
    uploaded_images_path = 'media/uploaded_images/'
    processed_images_path = 'media/processed_images/'
    
    empty_directories(uploaded_images_path, processed_images_path)
    
    original_image_path = ''
    try:
        # Getting image as input from the user 
        if request.method == 'POST':
            image_path = 'media/uploaded_images/'
            os.makedirs(image_path, exist_ok=True)
            
            image_file = request.FILES.get('image')
            image_path = os.path.join(image_path, image_file.name)
            
            with open(image_path, 'wb') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)
                    
            img = cv2.imread(image_path)
            
            if img is None:
                messages.error(request, "Image Not Found")
                return redirect('edge-detection')
            
            edge_detected_img = cv2.Canny(img, threshold1=100, threshold2=200)
            
            output_path = os.path.join(settings.BASE_DIR, f'media/processed_images/{image_file.name}')
            cv2.imwrite(output_path, edge_detected_img)
            
            
            original_image_path = f'/media/uploaded_images/{image_file.name}'
            request.session['original_image_path'] = original_image_path
            processed_image_path = f'/media/processed_images/{image_file.name}'
            context = {
                'processed_image_path' : processed_image_path,
                'original_image_path' : original_image_path,
            }
        
            return render(request, 'success.html', context=context)
        else:
            messages.error(request, "The Request was not correct")
    except Exception as e:
        messages.error(request, "Something went wrong")
        return redirect('edge-detection')
    return render(request, 'edge_detection.html')


# ------------------------------ Image Compression --------------------------------
def compress_image(request):
    uploaded_images_path = 'media/uploaded_images/'
    processed_images_path = 'media/processed_images/'
    
    empty_directories(uploaded_images_path, processed_images_path)
    
    original_image_path = ''
    try:
        # Getting image as input from the user 
        if request.method == 'POST':
            image_path = 'media/uploaded_images/'
            compress_range = int(request.POST.get('compress_range'))
            os.makedirs(image_path, exist_ok=True)
            
            # new_compress_range = int(compress_range)
            new_compress_range = compress_range // 2
            
            
            image_file = request.FILES.get('image')
            image_path = os.path.join(image_path, image_file.name)
            
            with open(image_path, 'wb') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)
                    
            img = cv2.imread(image_path)
            
            if img is None:
                messages.error(request, "Image Not Found")
                return redirect('compress-image')
            
            compression_params = [cv2.IMWRITE_JPEG_QUALITY, new_compress_range]
            
            output_path = os.path.join(settings.BASE_DIR, f'media/processed_images/{image_file.name}')
            cv2.imwrite(output_path, img, compression_params)
            
            request.session['original_image_path'] = original_image_path
            original_image_path = f'/media/uploaded_images/{image_file.name}'
            processed_image_path = f'/media/processed_images/{image_file.name}'
            context = {
                'processed_image_path' : processed_image_path,
                'original_image_path' : original_image_path,
            }
        
            return render(request, 'success.html', context=context)
        else:
            messages.error(request, "The Request was not correct")
    except Exception as e:
        messages.error(request, "Something went wrong")
        return redirect('compress-image')
    return render(request, 'image_compression.html')


# ------------------------ Convert PNG images to JPEG Image ------------------------
def convert_png_image(request):
    uploaded_images_path = 'media/uploaded_images/'
    processed_images_path = 'media/processed_images/'
    
    empty_directories(uploaded_images_path, processed_images_path)
    
    original_image_path = ''
    try:
        if request.method == 'POST':
            image_path = 'media/uploaded_images/'
            os.makedirs(image_path, exist_ok=True)
            
            image_file = request.FILES.get('image')
            image_path = os.path.join(image_path, image_file.name)
            
            with open(image_path, 'wb') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)
                    
            img = cv2.imread(image_path)
            
            if img is None:
                messages.error(request, "Image Not Found")
                return redirect('convert-png-to-jpg')
            
             # Define the output path for the JPG image
            output_path = os.path.join(settings.BASE_DIR, f'media/processed_images/{image_file.name.replace(".png", ".jpg")}')
            
            # Save the image in JPG format
            cv2.imwrite(output_path, img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
            
            request.session['original_image_path'] = original_image_path
            original_image_path = f'/media/uploaded_images/{image_file.name}'
            processed_image_path = f'/media/processed_images/{image_file.name.replace('.png', '.jpg')}'
            context = {
                'processed_image_path' : processed_image_path,
                'original_image_path' : original_image_path,
            }
        
            return render(request, 'success.html', context=context)
    except Exception as e:
        messages.error(request, "Something went wrong")
    return render(request, 'image_convert_png_to_jpg.html')


# -------------------------- Resize Image --------------------------------
def resize_image(request):
    uploaded_images_path = 'media/uploaded_images/'
    processed_images_path = 'media/processed_images/'
    
    empty_directories(uploaded_images_path, processed_images_path)
    
    original_image_path = ''
    try:
        if request.method == 'POST':
            width = request.POST.get('width')
            height = request.POST.get('height')
            aspect_ratio_checked = 'aspect_ratio' in request.POST
            image_path = 'media/uploaded_images/'
            os.makedirs(image_path, exist_ok=True)
            
            new_width = int(width)
            new_height = int(height) if not aspect_ratio_checked else None
            
            image_file = request.FILES.get('image')
            image_path = os.path.join(image_path, image_file.name)
            
            with open(image_path, 'wb') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)
                    
            img = cv2.imread(image_path)
            
            if img is None:
                messages.error(request, "Image Not Found")
                return redirect('resize-image')
            
            output_path = os.path.join(settings.BASE_DIR, f'media/processed_images/{image_file.name}')
            
            if aspect_ratio_checked:
                aspect_ratio = img.shape[1] / img.shape[0]
                new_height = int(new_width / aspect_ratio)
                resized_image = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
            else:
                resized_image = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
            
            cv2.imwrite(output_path, resized_image)
            
            
            request.session['original_image_path'] = original_image_path
            original_image_path = f'/media/uploaded_images/{image_file.name}'
            processed_image_path = f'/media/processed_images/{image_file.name.replace('.png', '.jpg')}'
            context = {
                'processed_image_path' : processed_image_path,
                'original_image_path' : original_image_path,
            }
        
            return render(request, 'success.html', context=context)
    except Exception as e:
        messages(request, "Something went wrong")
    return render(request, 'resize_image.html')


# --------------------------------- Convert from WEBP to JPG -----------------
def convert_webp_to_jpg(request):
    uploaded_images_path = 'media/uploaded_images/'
    processed_images_path = 'media/processed_images/'
    
    empty_directories(uploaded_images_path, processed_images_path)
    
    original_image_path = ''
    try:
        if request.method == 'POST':
            
            image_path = 'media/uploaded_images/'
            os.makedirs(image_path, exist_ok=True)
            
            image_file = request.FILES.get('image')
            image_path = os.path.join(image_path, image_file.name)
            
            with open(image_path, 'wb') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)
                    
            if not image_file.name.endswith(('.webp', '.WEBP')):
                messages.error(request, "Invalid file format. Please upload a webp image.")
                return redirect('convert-webp-to-jpg')
                    
            img = cv2.imread(image_path)
            
            if img is None:
                messages.error(request, "Image Not Found")
                return redirect('convert-webp-to-jpg')
            
            output_filename = os.path.splitext(image_file.name)[0] + '.jpg'
            output_path = os.path.join(settings.BASE_DIR, f'media/processed_images/{output_filename}')
            cv2.imwrite(output_path, img, [int(cv2.IMWRITE_JPEG_QUALITY), 80])  # Write as JPEG

            
            request.session['original_image_path'] = original_image_path
            original_image_path = f'/media/uploaded_images/{image_file.name}'
            processed_image_path = f'/media/processed_images/{output_filename}'
            context = {
                'processed_image_path' : processed_image_path,
                'original_image_path' : original_image_path,
            }
        
            return render(request, 'success.html', context=context)
    except Exception as e:
        messages(request, "Something went wrong")
    return render(request, 'webp_to_jpg.html')



# ---------------------- JPEG to WebP --------------------
def convert_jpg_to_webp(request):
    uploaded_images_path = 'media/uploaded_images/'
    processed_images_path = 'media/processed_images/'
    
    empty_directories(uploaded_images_path, processed_images_path)
    
    original_image_path = ''
    try:
        if request.method == 'POST':
            
            image_path = 'media/uploaded_images/'
            os.makedirs(image_path, exist_ok=True)
            
            image_file = request.FILES.get('image')
            image_path = os.path.join(image_path, image_file.name)
            
            with open(image_path, 'wb') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)
                    
            if not image_file.name.endswith(('.jpg', '.jpeg')):
                messages.error(request, "Invalid file format. Please upload a JPG image.")
                return redirect('convert-jpg-to-webp')

                    
            img = cv2.imread(image_path)
        
            output_filename = os.path.splitext(image_file.name)[0] + '.webp'
            output_path = os.path.join(settings.BASE_DIR, f'media/processed_images/{output_filename}')
            cv2.imwrite(output_path, img, [int(cv2.IMWRITE_WEBP_QUALITY), 80])
            
            request.session['original_image_path'] = original_image_path
            original_image_path = f'/media/uploaded_images/{image_file.name}'
            processed_image_path = f'/media/processed_images/{output_filename}'
            context = {
                'processed_image_path' : processed_image_path,
                'original_image_path' : original_image_path,
            }
        
            return render(request, 'success.html', context=context)
            
    except Exception as e:
        messages.error(request, "Something went wrong")
        print(e)
    return render(request, 'jpg_to_webp.html')

# Method to Empty Upload Image and Process Image Directory
def empty_directories(uploaded_images_path, processed_images_path):
    shutil.rmtree(uploaded_images_path, ignore_errors=True)
    shutil.rmtree(processed_images_path, ignore_errors=True)
    
    os.makedirs(uploaded_images_path, exist_ok=True)
    os.makedirs(processed_images_path, exist_ok=True)
    
    return True