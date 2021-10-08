from django.urls import path
from .views import EmailRegistrationView,  AccessTokenView


urlpatterns = [
    path('v1/auth/email/', EmailRegistrationView.as_view()),
    path('v1/auth/token/', AccessTokenView.as_view()),
]