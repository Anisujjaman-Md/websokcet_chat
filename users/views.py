from rest_framework import viewsets, status
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from .serializers import CustomTokenObtainPairSerializer, UserDetailSerializer, UserRegistrationSerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.core.cache import cache

User = get_user_model()

class UserRegistrationViewSet(CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = UserRegistrationSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token_data = serializer.to_representation(user)
            return Response(token_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CustomTokenObtainPairView(APIView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get the user object from validated data
        user_data = serializer.validated_data.get('user')

        if isinstance(user_data, dict):
            # User object is a dictionary, handle accordingly
            user_id = user_data.get('id')
            user_model = get_user_model()
            user = user_model.objects.get(id=user_id)
        else:
            # User object is an instance of Django user model
            user = user_data
        
        user_model.objects.filter(id=user.id).update(last_login=timezone.now())
        refresh = RefreshToken.for_user(user)

        return Response({
            'access_token': str(serializer.validated_data['access']),
            'refresh_token': str(refresh),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_staff': user.is_staff,
            }
        })
class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            refresh = RefreshToken(refresh_token)
            refresh.blacklist()

            # Issue a new access token
            new_access_token = refresh.access_token

            return Response(
                {
                    "message": "Logout successful",
                    "new_access_token": str(new_access_token),
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )
class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    @method_decorator(cache_page(1200, key_prefix="my_cache_prefix"))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)