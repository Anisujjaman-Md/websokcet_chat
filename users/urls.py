from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import CustomTokenObtainPairView, UserDetailView, UserRegistrationViewSet
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


router = DefaultRouter()
router.register(r'register', UserRegistrationViewSet, basename='register')

urlpatterns = [
    path('api/', include(router.urls)),
    
    #Login APIs
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    #User Details API : Need More Update
    path('api/user/', UserDetailView.as_view(), name='user_detail'),
]
