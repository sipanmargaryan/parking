from django.urls import path

from .views import auth, profile

app_name = 'users'
urlpatterns = [
    path('login/', auth.LogInAPIView.as_view(), name='login'),
    path('signup/', auth.SignupAPIView.as_view(), name='signup'),
]
