from django.urls import path, include
from .views import (
    AnswerListAPIView,
    QuestionAPIView,
    QuestionUpdateAPIView,
    CreateUserAPIView,
    CreateAdminAPIView,
)
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('qanswer/', AnswerListAPIView.as_view()),
    path('question/', QuestionAPIView.as_view()),
    path('question/<int:id>/', QuestionUpdateAPIView.as_view()),
]

# DRF auth paths
urlpatterns += [
    path('auth/', include('rest_framework.urls')),
    path('register/', CreateUserAPIView.as_view(), name='register'),
    path('admin-register/', CreateAdminAPIView.as_view(), name='admin-register'),
    path('get-auth-token/', obtain_auth_token, name='get_auth_token'),
]