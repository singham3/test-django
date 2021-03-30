from rest_framework.response import Response
from rest_framework import status
from .serializer import AuthUserSerializer
from rest_framework.decorators import api_view
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .middleware import *
from datetime import datetime
from django.core.paginator import Paginator
from django.utils.decorators import decorator_from_middleware, decorator_from_middleware_with_args
from .models import User


@api_view(['POST'])
@decorator_from_middleware(UserMiddleware)
def user_create_view(request, form, pk=None):
    serializer = AuthUserSerializer(data=form.cleaned_data)
    if serializer.is_valid():
        serializer.save()
        return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)
    else:
        data = {"data": serializer._errors}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@decorator_from_middleware(UserLoginMiddleware)
def user_login_view(request, form):
    email = form.cleaned_data['email']
    password = form.cleaned_data['password']
    user_obj = User.objects.get(email=email)
    if user_obj.check_password(password):
        serializer = TokenObtainPairSerializer(data=form.cleaned_data)
        token = serializer.validate({'email': email, 'password': password})
        user_obj.last_login = datetime.now()
        user_obj.save()
        serializer = AuthUserSerializer(instance=user_obj, many=False)
        data = {'user': serializer.data, 'token': token['access']}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"data": "Password is not Correct"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'], )
@decorator_from_middleware(TokenMiddleware)
def user_list_view(request):
    page = 1 if 'page' not in request.GET else 1 if not request.GET['page'] else request.GET['page']
    limit = 5 if 'limit' not in request.GET else 5 if not request.GET['limit'] else request.GET['limit']
    if request.user.is_superuser:
        user_obj = User.objects.all()
        paginator = Paginator(user_obj, limit)
        users = paginator.page(page)
        serializer = AuthUserSerializer(instance=users, many=True)
        data = {'users': serializer.data}
        return Response(data, status=status.HTTP_200_OK)
    return Response({'data': 'Unauthorized request'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'], )
@decorator_from_middleware(TokenMiddleware)
def user_detail_view(request):
    serializer = AuthUserSerializer(instance=request.user, many=False)
    data = {'users': serializer.data}
    return Response(data, status=status.HTTP_200_OK)


