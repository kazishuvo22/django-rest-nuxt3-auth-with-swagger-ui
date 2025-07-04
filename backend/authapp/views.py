from datetime import timedelta

from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken
from authapp.models import CustomUser, CustomUserDetails
from authapp.serializers import CustomUserSerializer, CustomUserDetailsSerializer, UserRegistrationSerializer, \
    LoginSerializer
from ecomweb import settings


class UserViewSet(viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer  # Default serializer; can be overridden
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Get logged-in user data along with details.
        GET /users/me/
        """
        user = request.user
        user_details = CustomUserDetails.objects.filter(user=user).first()
        details_data = None
        if user_details:
            details_data = CustomUserDetailsSerializer(user_details).data

        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_verified': user.is_verified,
            'details': details_data,
        })

    @action(detail=False, methods=['put'], permission_classes=[IsAuthenticated])
    def update_details(self, request):
        """
        Update logged-in user and user details.
        PUT /users/update_details/
        """
        user = request.user

        user_serializer = CustomUserSerializer(user, data=request.data, partial=True)

        user_details = CustomUserDetails.objects.get(user=user)
        details_data = request.data.get("details", {})
        details_serializer = CustomUserDetailsSerializer(user_details, data=details_data, partial=True)

        user_valid = user_serializer.is_valid()
        details_valid = details_serializer.is_valid()

        if user_valid and details_valid:
            user_serializer.save()
            details_serializer.save()
            return Response({
                "message": "User details updated successfully.",
                "user": user_serializer.data,
                "details": details_serializer.data,
            }, status=status.HTTP_200_OK)

        errors = {}
        if not user_valid:
            errors["user_errors"] = user_serializer.errors
        if not details_valid:
            errors["details_errors"] = details_serializer.errors

        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class LoginViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        identifier = serializer.validated_data['username_or_email']
        password = serializer.validated_data['password']

        try:
            user_obj = CustomUser.objects.get(Q(username=identifier) | Q(email=identifier))
        except CustomUser.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=user_obj.username, password=password)
        if not user:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        # Get token lifetime (expiration) from settings (in seconds)
        access_token_lifetime = settings.SIMPLE_JWT.get('ACCESS_TOKEN_LIFETIME', timedelta(minutes=5))
        expires_in = int(access_token_lifetime.total_seconds())

        return Response({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_active': user.is_active,
                'is_staff': user.is_staff,
                'is_superuser': user.is_superuser
            },
            'access_token': str(access_token),
            'refresh_token': str(refresh),
            'expires_in': expires_in,  # seconds until expiry
        }, status=status.HTTP_200_OK)


class RegisterViewSet(viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            return Response({"error": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.save()
        return Response({
            "message": "User registered successfully.",
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_staff": user.is_staff,
            "is_active": user.is_active
        }, status=status.HTTP_201_CREATED)
