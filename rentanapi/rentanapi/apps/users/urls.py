from django.urls import path, re_path
from rest_framework_jwt.views import obtain_jwt_token

from users import views

urlpatterns = [
    path(r'login/', obtain_jwt_token),
    path("captcha/", views.CaptchaAPIView.as_view()),
    re_path("sms/(?P<mobile>1[3-9]\d{9})/", views.SMSCodeAPIView.as_view()),
    path('', views.UserCreateAPIView.as_view()),
    path('find/password/', views.ResetPasswordAPIView.as_view()),
]