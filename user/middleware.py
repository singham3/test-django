import os, sys
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication

View_class = ['UserCreateAPIView', 'UserLoginAPIView']


class CommonMiddleware(MiddlewareMixin):
    def process_request(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)

    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            if request.user.is_authenticated:
                return None
            if view_func.__name__ not in View_class:
                jwt_object = JWTAuthentication()
                header = jwt_object.get_header(request)
                print("header == ", header)
                if header is not None:
                    raw_token = jwt_object.get_raw_token(header)
                    print("raw_token = ", raw_token)
                    validated_token = jwt_object.get_validated_token(raw_token)
                    print("validated_token == ", validated_token)
                    request.user = jwt_object.get_user(validated_token)
                    print("request.user === ", request.user)
                    return None
                return JsonResponse({'error': "Invalid Token"}, status=200)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return JsonResponse({'error': f"{e}, {f_name}, {exc_tb.tb_lineno}"}, status=200)
