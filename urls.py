from django.urls import path
from . import views

urlpatterns = [
    path('', views.process_image, name='process_image'), 
    path('process-image', views.process_image, name='process_image'), 
    path('about', views.about, name='about'), 
]
