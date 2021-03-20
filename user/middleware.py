import os, sys
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication

View_class = ['UserCreateAPIView','UserLoginAPIView']


class CommonMiddleware(MiddlewareMixin):
    def process_request(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)

    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            # print('+++',request.user)
            if request.user.is_authenticated:
                return None
            # print(list(view_func))
            if view_func.__name__ not in View_class:
                print(request.user , request.user.is_authenticated)
                if bool(request.user and request.user.is_authenticated):
                    # raw_token = jwt_object.get_raw_token(header)
                    # validated_token = jwt_object.get_validated_token(raw_token)
                    # request.user = jwt_object.get_user(validated_token)
                    # # if request.user.token != str(validated_token):
                    # #     return JsonResponse({'error': "User Not Login"}, status=200)
                    return None
                return JsonResponse({'error': "Invalid Token"}, status=200)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return JsonResponse({'error': f"{e}, {f_name}, {exc_tb.tb_lineno}"}, status=200)
