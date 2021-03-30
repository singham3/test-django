from django.utils.deprecation import MiddlewareMixin
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from .forms import *


class TokenMiddleware(MiddlewareMixin):
    def process_request(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)

    def process_view(self, request, view_func, view_args, view_kwargs):
        jwt_object = JWTAuthentication()
        header = jwt_object.get_header(request)
        if header is not None:
            raw_token = jwt_object.get_raw_token(header)
            validated_token = jwt_object.get_validated_token(raw_token)
            request.user = jwt_object.get_user(validated_token)
            return None
        return Response({'error': "Invalid Token"}, status=200)

    def process_exception(self, request, exception):
        return Response({'error': exception.message}, status=200)


class UserMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        pk = view_kwargs['pk'] if 'pk' in view_kwargs else None
        if request.method in ("POST", "PUT"):
            user = request.user if request.user.is_authenticated else None
            form = UserRegisterForm(data=request.data, instance=user, files=request.FILES)
            if form.is_valid():
                return view_func(request, form, pk)
            else:
                return Response({'error': form.errors.as_json()}, status=200)
        else:
            return view_func(request, None, pk)

    def process_exception(self, request, exception):
        return Response({'error': exception.message}, status=200)


class UserLoginMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        form = UserLoginForm(data=request.data)
        if form.is_valid():
            return view_func(request, form)
        else:
            return Response({'error': form.errors.as_json()}, status=200)

    def process_exception(self, request, exception):
        print(exception.message, exception.__class__.__name__)
        return Response({'error': exception.message}, status=200)

