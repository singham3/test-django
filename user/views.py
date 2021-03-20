from rest_framework.response import Response
from rest_framework import status
from .serializer import AuthUserSerializer
from rest_framework.decorators import api_view
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import hashers
from .forms import *
from django.core import serializers
import json


@api_view(['POST'], )
def UserCreateAPIView(request):
    form = UserRegisterForm(data=request.POST)
    if form.is_valid():
        data = {'username': request.data['username'], 'email': request.data['email'],
                'password': request.data['password']}
        serializer = AuthUserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'signup successful'}, status=status.HTTP_201_CREATED)
        else:
            data = {"data": serializer._errors}
            print(data)
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    data = {'data': form._errors}
    print(data)
    return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'], )
def UserLoginAPIView(request):
    if User.objects.filter(email=request.data['email']).exists():
        user_obj = User.objects.get(email=request.data['email'])
        if user_obj.check_password(request.data['password']):
            serializer = TokenObtainPairSerializer(
                data={'email': request.data['email'], 'password': request.data['password']})
            token = serializer.validate({'username': user_obj.username, 'password': request.data['password']})
            print(token)
            data = {'email': request.data['email'], 'token': token['access']}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    data = {'data': 'Invalid user'}
    print(data)
    return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'], )
def UserListAPIView(request):
    if request.user.is_superuser:
        user_obj = User.objects.all()
        user_list = AuthUserSerializer(instance=user_obj)
        data = {'users': user_list}
        return Response(data, status=status.HTTP_200_OK)
    data = {'data': 'Unauthorized request'}
    print(data)
    return Response(data, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'], )
def UserDetailAPIView(request):
    print(request.user)
    if User.objects.filter(username=request.user).exists():
        user_obj = User.objects.get(id=request.user.id)
        if user_obj.is_superuser:
            user_obj = User.objects.all()
            user_list = serializers.serialize('json', user_obj)
            data = {'users': user_list}
            return Response(data, status=status.HTTP_200_OK)
        else:
            user_list = json.loads(serializers.serialize('json', [user_obj], ensure_ascii=False))
            print(user_list[0]['fields'])
            del user_list[0]['fields']['password']
            data = {'users': user_list}
            return Response(data, status=status.HTTP_200_OK)
    data = {'data': 'Invalid request'}
    print(data)
    return Response(data, status=status.HTTP_400_BAD_REQUEST)


from django.shortcuts import render

# Create your views here.
