from django.urls import path
from .views import RegisterView
from .views import LoginView
from .views import AccountInfoView,SideProfileView,UserProductListView,UserStatsView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view()),
    path('account-info/', AccountInfoView.as_view(), name='account-info'),
    path('side-profile/', SideProfileView.as_view(), name='side-profile'),
    path('my-products/', UserProductListView.as_view(), name='user-products'),
    path('user-stats/', UserStatsView.as_view(), name='user-stats'),


]
