from django.http import HttpResponse
from django.shortcuts import render

import numpy as np
import math
import cv2
import operator
from PIL import Image as Image
from matplotlib import pyplot as mpl

#Kernel List
Kernel_Sharpen = [0,-1,0,-1,5,-1,0,-1,0]
Kernel_Emboss = [-2,-1,0,-1,1,1,0,1,2]
Kernel_Lighten = [0,0,0,0,1.5,0,0,0,0]
Kernel_Darken = [0,0,0,0,0.5,0,0,0,0]
Kernel_EdgeDetection = [0,1,0,1,-4,1,0,1,0]

def Matrix_Multiply(matrix,multiplier) :
    result = []
    for element in matrix:
      multiply = (float(element) * multiplier)
      result.append(int(multiply))
    return result

def MultiplyMatrixWithKernel(file, kernel=[]):
    img = Image.open(file).convert('RGB')
    new_img = img.copy()
    width, height = img.size
    kernel_size = int(math.sqrt(len(kernel))) 
    kernel_center = kernel_size // 2
    
    for x in range(kernel_center, width - kernel_center):
        for y in range(kernel_center, height - kernel_center):
            sum_pixels = (0, 0, 0)
            for i in range(kernel_size):
                for j in range(kernel_size):
                    pixel = (x + j - kernel_center, y + i - kernel_center)
                    value = Matrix_Multiply(img.getpixel(pixel), kernel[i * kernel_size + j])
                    sum_pixels = tuple(map(operator.add, sum_pixels, value))
            new_img.putpixel((x, y), tuple(sum_pixels))
    
    return new_img

def ImageSharpen(file) :
  result = MultiplyMatrixWithKernel(file,Kernel_Sharpen)
  return result

def ImageEmboss(file) :
  result = MultiplyMatrixWithKernel(file,Kernel_Emboss)
  return result

def ImageLighten(file) :
  result = MultiplyMatrixWithKernel(file,Kernel_Lighten)
  return result

def ImageDarken(file) :
  result = MultiplyMatrixWithKernel(file,Kernel_Darken)
  return result

def ImageEdgeDetection(file) :
  result = MultiplyMatrixWithKernel(file,Kernel_EdgeDetection)
  return result

def GrayScale(file):
  img = Image.open(file).convert('RGB')
  width, height = img.size
  new_img = img.copy().convert('L')
  for x in range(0, width-1):
    for y in range(0, height-1):
      r,g,b = img.getpixel((x,y))
      luminance = 0.299*r + 0.587*g + 0.114*b
      luminance = int(luminance)
      new_img.putpixel((x,y),luminance)
  return new_img


def process_image(request):
    if request.method == 'POST':
       
        uploaded_file = request.FILES['image']
        
        processing_method = request.POST.get('processing_method')
        
        if processing_method == 'sharpen':
            processed_image = ImageSharpen(uploaded_file)
        elif processing_method == 'emboss':
            processed_image = ImageEmboss(uploaded_file)
        elif processing_method == 'lighten':
            processed_image = ImageLighten(uploaded_file)
        elif processing_method == 'darken':
            processed_image = ImageDarken(uploaded_file)
        elif processing_method == 'edge_detection':
            processed_image = ImageEdgeDetection(uploaded_file)
        elif processing_method == 'grayscale':
            processed_image = GrayScale(uploaded_file)
        
        response = HttpResponse(content_type='image/png')
        processed_image.save(response, 'PNG')
        return response
    
    return render(request, 'process_image.html')


def about(request):
    return render(request, 'about.html')