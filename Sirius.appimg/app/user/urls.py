from django.urls import path
from rest_framework_jwt.views import ObtainJSONWebToken, RefreshJSONWebToken, VerifyJSONWebToken
from .views import UserProfileView, UserCreateView, UserCurrentView, UserProfileCreateView

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name="userpage"),
    path('create-profile/', UserProfileCreateView.as_view(), name="create userpage"),
    path('register/', UserCreateView.as_view(), name="create-user"),
    path('current_user/', UserCurrentView.as_view(), name="verify-token"),
    path('api-token-auth/', ObtainJSONWebToken.as_view(), name="obtain-token"),
    path('api-token-refresh/', RefreshJSONWebToken.as_view(), name="refresh-token"),
    path('api-token-verify/', VerifyJSONWebToken.as_view(), name="verify-token"),
]
