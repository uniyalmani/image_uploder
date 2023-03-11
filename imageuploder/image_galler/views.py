from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.parsers import MultiPartParser
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import UploadedImage
# from auth_app.serializers.user_serializer import UserSerializer
from imageuploder.settings import aws_access_key_id, aws_secret_access_key, bucket_name
import jwt, datetime
from image_galler.utilities.helpers import create_aws_client, upload_file_to_s3_bucket, delete_image_from_s3
from django.shortcuts import redirect
from django.contrib import messages
import jwt
# Create your views here.



class UploadImage(APIView):

    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]
    authentication_classes = [JWTAuthentication]

    parser_classes = [MultiPartParser]
    permission_classes = [AllowAny]
    def post(self, request):
        print("post started ", request.info)
        if not request.info["valid"]:
            messages.error(request, 'Invalid token. for uploading images please loging')
            return redirect('/auth/login')
        
        s3 = create_aws_client(aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key)
    
       
        
        file = request.FILES['image']
        print(request.data, file)
        upload_info = upload_file_to_s3_bucket(s3_client=s3, bucket_name=bucket_name, file= file)
       
        image_key, image_url = upload_info["object_key"], upload_info["url"]
        print(request.info["user"].email,type(request.info["user"].email) , "value of email ")

        uploaded_image = UploadedImage(user_email = request.info["user"],
                                        image_key = image_key,
                                        image_url=  image_url,
                                        image_title =request.data["image_name"],
                                        image_description = request.data["image_description"]
                                        )
        uploaded_image.save()
        # print(upload_info, "url", "llllll")
        # res = delete_image_from_s3(s3, upload_info["object_key"], bucket_name=bucket_name)
        # print(res, "ppppp")
        return redirect('/user/images')

    def get(self, request):
        response = render(request, template_name="image_upload.html")
        return response
    


    



    
class ViewImages(APIView):

    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]
    authentication_classes = [JWTAuthentication]

    # parser_classes = [MultiPartParser]
    permission_classes = [AllowAny]

    def get(self, request):
        
        if not request.info["valid"]:
            messages.error(request, 'Invalid token. for viewing images please loging')
            return redirect('/auth/login')
        
        user_email = request.info["user"].email
        images = UploadedImage.objects.filter(user_email=user_email).order_by('-created_at')

        context = {"user_images": images}
        return render(request, template_name="images.html", context=context)
    


def delete_image(request, pk):
    # image = get_object_or_404(Image, image_key=pk)
    print(pk, "value of pk")
    UploadedImage.objects.filter(image_key=pk).delete()
    s3 = create_aws_client(aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key)
    


    res = delete_image_from_s3(s3, pk, bucket_name=bucket_name)

    return redirect('/user/images')

def home(request):

    return render(request, template_name="home.html")
    

def profile(request):
    return render(request, template_name="profile.html")