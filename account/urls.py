from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from .views import RegistrationView, SelfAccountView, AccountView

app_name = "account"

urlpatterns = [    
    path('register/', RegistrationView.as_view(), name='RegistrationView'),
    path('login/', obtain_auth_token, name='LoginView'),
    
    path('profile/', SelfAccountView.as_view(), name="SelfAccountView"),
    path('profile/<int:id>/', AccountView.as_view(), name="AccountView"),


]