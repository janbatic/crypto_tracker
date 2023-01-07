from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework import permissions
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from core.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token as AuthToken


class RegisterView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        data = request.data
        if not data:
            return HttpResponse(status=400, content="No data given")

        validation = self.registration_validation(data)
        if isinstance(validation, HttpResponse):
            return validation

        try:
            user = User.objects.create_user(
                username=data.get("username"),
                email=data.get("email"),
                password=data.get("password")
            )
        except Exception as e:
            return HttpResponse(status=409, content=e)

        auth_token, created = AuthToken.objects.get_or_create(user=user)
        return JsonResponse(
            {
                "Bearer": auth_token.key
            }
        )

    @staticmethod
    def registration_validation(data):
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        password_again = data.get("password_again")
        if not username:
            return HttpResponse(status=400, content="No parameter username given")
        if not email:
            return HttpResponse(status=400, content="No parameter email given")
        if not password:
            return HttpResponse(status=400, content="No parameter password given")
        if not password_again:
            return HttpResponse(status=400, content="No parameter password_again given")
        if not (password == password_again):
            return HttpResponse(status=400, content="Passwords are not matching")
        try:
            validate_password(password)
        except ValidationError as e:
            return HttpResponse(status=409, content=e)
        try:
            validate_email(email)
        except ValidationError as e:
            return HttpResponse(status=409, content=e)
        user_exists = User.objects.filter(username=username)
        if user_exists:
            return HttpResponse(status=409, content="User with this username already exists")
        user_exists = User.objects.filter(email=email)
        if user_exists:
            return HttpResponse(status=409, content="User with this email already exists")
        return True


class LoginView(APIView):
    permission_classes = (permissions.AllowAny, )

    @staticmethod
    def post(request):
        data = request.data
        if not data:
            return HttpResponse(status=400, content="No data given")
        username = data.get("username")
        password = data.get("password")
        if not username:
            return HttpResponse(status=400, content="No parameter username given")
        if not password:
            return HttpResponse(status=400, content="No parameter password given")

        user = authenticate(request, username=username, password=password)
        if not user:
            return HttpResponse(status=401, content="Wrong combination of password and username given")
        auth_token, created = AuthToken.objects.get_or_create(user=user)
        return JsonResponse(
            {
                "Bearer": auth_token.key
            }
        )


class LogoutView(APIView):

    permission_classes = [permissions.IsAuthenticated]
    @staticmethod
    def post(request):
        bearer = request.META.get('HTTP_AUTHORIZATION')
        token = bearer.split(' ')[1]
        AuthToken.objects.get(key=token).delete()
        return HttpResponse(status=200)


