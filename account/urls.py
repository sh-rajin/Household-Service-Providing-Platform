from django.urls import path, include
from .views import RegistrationAPIView, LoginAPIView, LogoutAPIView, activate

urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name="register"),
    path('login/', LoginAPIView.as_view(), name="login"),
    path('logout/', LogoutAPIView.as_view(), name="logout"),
    path('activate/<uidb64>/<token>/', activate, name="activate"),
]