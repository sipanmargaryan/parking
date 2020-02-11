from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path, include

from .views import auth, profile

auth_patterns = [
    path('login/', auth.LogInAPIView.as_view(), name='login'),
    path('signup/', auth.SignupAPIView.as_view(), name='signup'),
    path('forgot-password/', auth.ForgotPasswordAPIView.as_view(), name='forgot_password'),
    path('confirm-phone/', auth.ConfirmPhoneNumberAPIView.as_view(), name='confirm_phone_number'),
    path('reset-password/', auth.ResetPasswordAPIView.as_view(), name='reset_password'),
    path('refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
]

profile_patterns = [
    path('change-password/', profile.ChangePasswordAPIView.as_view(), name='change_password'),
    path(
            'change-avatar/',
            profile.ChangeAvatarViewSet.as_view({
                'post': 'update',
            }),
            name='change_avatar'
        ),
    path('add-car/', profile.AddCarAPIView.as_view(), name='add_car'),
    path('edit_car/<int:pk>/', profile.EditCarAPIView.as_view(), name='edit_car'),
]

app_name = 'users'
urlpatterns = [
    path('', include(auth_patterns)),
    path('', include(profile_patterns)),
]
