from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework import authentication, permissions
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from .models import User
from auth_app.serializers.user_serializer import UserSerializer, UserLoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages
import jwt, datetime

# Create your views here.

#generate token 
def get_tokens_for_user(user):
    print(user, "user inside login ", user.name, user.email, user.id)
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class SignUp(APIView):

    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]
    permission_classes = [AllowAny]

    def get(self, request):
        return render(request, template_name="auth_app/signup.html")


    def post(self, request):
        response = HttpResponse()
        
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            response = HttpResponseRedirect('/user/uplod_image')
            response['Authorization'] = 'Bearer ' + str(token["refresh"])
            response.set_cookie('jwt', str(token["access"]))
            return response
        
        messages.error(request, 'please try again email already exist or create account with new email')
        return redirect('/auth/signup', permanent=False, **response)

class Login(APIView):
   
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]
    permission_classes = [AllowAny]

    def post(self, request):
        print(request.data, "data")
        serializer = UserLoginSerializer(data=request.data)
        # response = HttpResponse(status=302)
        if serializer.is_valid(raise_exception=True):
            email= serializer.data.get("email")
            password = serializer.data.get("password")
            user = authenticate(email=email, password=password)
            
            if user is not None:
                token = get_tokens_for_user(user)
                response = HttpResponseRedirect('/user/uplod_image')
                response.set_cookie('jwt', str(token["access"]))
                return response
            
        response['Location'] = '/auth/login'
        messages.error(request, 'wrong email or password try again')
        return HttpResponseRedirect('/auth/login')
        

    def get(self, request):
        return render(request, template_name="auth_app/login.html")
    




def logout(request):
    # image = get_object_or_404(Image, image_key=pk)
    response = HttpResponseRedirect('/user/home')
    response.delete_cookie('jwt')

    return response
