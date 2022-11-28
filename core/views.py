import requests
from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from core.models import User


class RegisterView(APIView):
    @staticmethod
    def post(request):
        data = request.data
        if not data:
            return HttpResponse(status=400, content='No data given')
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        password_again = data.get('password_again')
        if not username:
            return HttpResponse(status=400, content='No parameter username given')
        if not email:
            return HttpResponse(status=400, content='No parameter email given')
        if not password:
            return HttpResponse(status=400, content='No parameter password given')
        if not password_again:
            return HttpResponse(status=400, content='No parameter password_again given')
        if not (password == password_again):
            return HttpResponse(status=400, content='Passwords are not matching')
        try:
            validate_password(password)
        except ValidationError as e:
            return HttpResponse(status=409, content=e)
        user_exists = User.objects.filter(username=username)
        if user_exists:
            return HttpResponse(status=409, content='User with this username already exists')
        user_exists = User.objects.filter(email=email)
        if user_exists:
            return HttpResponse(status=409, content='User with this email already exists')

        user = User().create_user(username=username, email=email, password=password, password_again=password_again)
        if isinstance(user, User):
            return HttpResponse(status=200)
        return HttpResponse(status=409)
