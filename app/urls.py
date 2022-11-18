from django.urls import path
from app.views.user import (
     LoginView, RetrieveUserAPI, ListUserAPI, RefreshTokenView, SignUpAPI,
     DeleteUserAPI, UpdateUserAPI, ResetPasswordView)
from dj_rest_auth.views import PasswordChangeView, PasswordResetConfirmView

urlpatterns = [

     path('token/refresh', RefreshTokenView.as_view(), name='token_refresh'),
     path('user/login', LoginView.as_view(), name='login'),
     path('user/adduser', SignUpAPI.as_view(), name='add_user'),
     path('user/updateuser/<id>', UpdateUserAPI.as_view(), name='update_user'),
     path('user/deleteuser/<id>', DeleteUserAPI.as_view(), name='delete_user'),
     path('user/getuser/<id>',

          RetrieveUserAPI.as_view(), name='get-user-by-id'),
     path('user/allusers', ListUserAPI.as_view(), name='listusers'),
     path('user/changepassword', PasswordChangeView.as_view(),
          name='password_change'),
     path('user/resetpassword', ResetPasswordView.as_view(),
          name='password_reset'),
     path('user/resetpasswordconfirm/<uidb64>/<token>',
          PasswordResetConfirmView.as_view(),
          {'template_name': 'registration/password_reset_email.html'},
          name='password_reset_confirm'),
]