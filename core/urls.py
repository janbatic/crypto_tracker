from django.urls import path
from .views import RegisterView, LoginView, LogoutView

urlpatterns = [
    path('user/register/', RegisterView.as_view()),
    path('user/login/', LoginView.as_view()),
    path('user/logout/', LogoutView.as_view()),
]