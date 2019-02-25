from django.urls import path
from basic_app import views

app_name = 'basic_app'

urlpatterns = [
    path(r'register/',views.register,name='register'),
    path(r'user_login/',views.user_login,name="user_login")
]