from django.utils.deprecation import MiddlewareMixin

# class JwtTokenMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         jwt_token = request.COOKIES.get('jwt_token')
#         if jwt_token:
#             request.META['Authorization'] = 'Bearer ' + jwt_token
#         return None



from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils.functional import SimpleLazyObject
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from django.utils.translation import gettext_lazy as _

class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        """
        Returns a two-tuple of `User` and token if a valid signature has been
        supplied using JWT based authentication.  Otherwise returns `None`.
        """
        # Get the token from the cookie
        jwt_token = request.COOKIES.get('jwt')

        if jwt_token is None:
            return None

        # Verify the token and decode its payload
        try:
            validated_token = self.get_validated_token(jwt_token)
        except AuthenticationFailed as exc:
            # raise AuthenticationFailed(_('Invalid token')) from exc
            return None, None

        # Extract the user data from the decoded token's payload
        user_data = validated_token.payload

        # Get the user object from the user ID stored in the token's payload
        User = get_user_model()
        try:
            user = User.objects.get(pk=user_data['user_id'])
        except User.DoesNotExist:
            raise AuthenticationFailed(_('User not found'))

        print(user, " insdied middle wer f")
        return (user, validated_token)


class CookieJWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.info = SimpleLazyObject(lambda: self.__class__.get_user(request))
        print(request.user, "imsde moddfsadf jdfj", request.info)
        response = self.get_response(request)
        return response

    @staticmethod
    def get_user(request):
        User = get_user_model()
        data = {"valid": False, "user": None}
        try:
            jwt_token = request.COOKIES.get('jwt')
            if jwt_token:
                user, validated_token = CookieJWTAuthentication().authenticate(request)
                print(user, validated_token, "/////////")
                if user:
                    data["valid"] = True
                    data["user"] = user
        except AuthenticationFailed as e:
            print(e, "middlkll")
        except Exception as e:
            print(e, "middlkll")
        
        return data