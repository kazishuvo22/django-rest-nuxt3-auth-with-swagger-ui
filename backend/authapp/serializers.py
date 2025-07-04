from rest_framework import serializers
from .models import CustomUser, CustomUserDetails


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 'last_name']

    def validate_password(self, value):
        # Custom password validation rules
        if len(value) < 6:
            raise serializers.ValidationError("Password must be at least 6 characters long.")
        # if not any(char.isupper() for char in value):
        #     raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("Password must contain at least one digit.")
        # if not any(char.islower() for char in value):
        #     raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        # Optional: Ensure password has no whitespace
        if " " in value:
            raise serializers.ValidationError("Password cannot contain spaces.")
        # Optional: Enforce a special character requirement
        # if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
        #     raise serializers.ValidationError("Password must contain at least one special character.")
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password_confirm": "Passwords must match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            password=validated_data['password']
        )
        return user


class CustomUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name']

    def validate_email(self, value):
        user = self.instance  # current user instance (if updating)
        if CustomUser.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value


class CustomUserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserDetails
        fields = ['full_name', 'phone', 'address', 'city', 'state', 'country', 'postal_code']


class LoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)