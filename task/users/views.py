from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import RegistrationForm, LoginForm
from .serializers import UserRegistrationSerializer
from rest_framework import status
from django.contrib import messages
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView



class UserRegistrationAPIView(CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                ## You can use this handler when you want to get token in postman or ...
                # jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                # jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
                # payload = jwt_payload_handler(user)
                # token = jwt_encode_handler(payload)
                # return JsonResponse({'token': token})
                return JsonResponse({'message': 'Login successful'})
            else:
                return JsonResponse({'error': 'Invalid username or password'}, status=401)
    return JsonResponse({'error': 'Invalid request'}, status=400)
