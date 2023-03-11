from django.urls import path
from .views import *


urlpatterns = [
    path('uplod_image', UploadImage.as_view(), name='upload-image'),
    path('images', ViewImages.as_view(), name='images'),
    path('images/<str:pk>', delete_image, name="delete_image"),
    path('home', home, name='home'),
    path('profile', profile, name='profile'),
]