from django.urls import path
from .views import RegisterView
from .views import LoginView
from .views import UserProfileView, AccountInfoView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view()),
    path('userprofile/', UserProfileView.as_view(), name='user-profile'),
    path('account-info/', AccountInfoView.as_view(), name='account-info'),

]
