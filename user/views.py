from rest_framework.response import Response
from rest_framework import status
from .serializer import AuthUserSerializer
from rest_framework.decorators import api_view
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .forms import *
from datetime import datetime
from django.core.paginator import Paginator


@api_view(['POST'], )
def UserCreateAPIView(request):
    form = UserRegisterForm(data=request.POST)
    if form.is_valid():
        serializer = AuthUserSerializer(data=form.cleaned_data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'successfully signup'}, status=status.HTTP_201_CREATED)
        else:
            data = {"data": serializer._errors}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    data = {'data': form._errors}
    return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'], )
def UserLoginAPIView(request):
    if User.objects.filter(email=request.data['email']).exists():
        user_obj = User.objects.get(email=request.data['email'])
        if user_obj.check_password(request.data['password']):
            serializer = TokenObtainPairSerializer(data=request.data)
            token = serializer.validate({'username': user_obj.username, 'password': request.data['password']})
            user_obj.last_login = datetime.now()
            user_obj.save()
            serializer = AuthUserSerializer(instance=user_obj, many=False)
            data = {'user': serializer.data, 'token': token['access']}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        data = {'data': 'Invalid User'}
    return Response(data, status=status.HTTP_400_BAD_REQUEST)


# localhost:8888/api/v1/user/list/?page=1&limit=10
@api_view(['GET'], )
def UserListAPIView(request):
    page = 1 if 'page' not in request.GET else 1 if not request.GET['page'] else request.GET['page']
    limit = 5 if 'limit' not in request.GET else 5 if not request.GET['limit'] else request.GET['limit']
    if request.user.is_superuser:
        user_obj = User.objects.all()
        paginator = Paginator(user_obj, limit)
        users = paginator.page(page)
        serializer = AuthUserSerializer(instance=users, many=True)
        data = {'users': serializer.data}
        return Response(data, status=status.HTTP_200_OK)
    data = {'data': 'Unauthorized request'}
    return Response(data, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'], )
def UserDetailAPIView(request):
    serializer = AuthUserSerializer(instance=request.user, many=False)
    data = {'users': serializer.data}
    return Response(data, status=status.HTTP_200_OK)


