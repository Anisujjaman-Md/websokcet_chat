from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import CustomTokenObtainPairView, LogoutAPIView, UserDetailView, UserRegistrationViewSet
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


router = DefaultRouter()
router.register(r'register', UserRegistrationViewSet, basename='register')

urlpatterns = [
    path('', include(router.urls)),
    
    #Login APIs
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    
    #User Details API : Need More Update
    path('user/', UserDetailView.as_view(), name='user_detail'),
]
