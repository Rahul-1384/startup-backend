from django.urls import path
from account.views import (
    UserRegistrationView,
    UserLoginView,
    UserProfileView,
    UserChangePasswordView,
    SetPasswordResetEmailView,
    UserSetPasswordResetView,
)    

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('set-reset-password-email/', SetPasswordResetEmailView.as_view(), name='set-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserSetPasswordResetView.as_view(), name='reset-password'),
]
