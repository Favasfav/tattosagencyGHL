from rest_framework import serializers

from rest_framework.serializers import ModelSerializer, ValidationError, ImageField
# from base.models import Note
# from django.contrib.auth.models import User
from .models import CustomUser,Appointment


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    

 


class SignupSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ['email','username','password']
        extra_kwargs = {
            'password':{'write_only':True}
        }


# from rest_framework import serializers
# from django.core.exceptions import ValidationError
# from .models import CustomUser

# class SignupSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = CustomUser
#         fields = ['email', 'username', 'password']
#         extra_kwargs = {
#             'password': {'write_only': True},  # Ensure password is write-only
#         }

#     def validate_email(self, value):
#         """
#         Validate the email to check if the user already exists.
#         If the email exists and no password is set, update the password.
#         """
#         existing_user = CustomUser.objects.filter(email=value).first()

#         if existing_user:
#             # If user exists and no password is set, set the password
#             if not existing_user.password and 'password' in self.initial_data:
#                 existing_user.set_password(self.initial_data['password'])
#                 existing_user.save()
#             # If the user exists, we don't need to raise an error here.
#             # Just return the email value.
#         return value

#     def validate(self, attrs):
#         """
#         Additional validation to check if the password is provided.
#         """
#         if 'password' not in attrs or not attrs.get('password'):
#             raise ValidationError({"password": "Password is required."})
        
#         return attrs

#     def create(self, validated_data):
#         """
#         Create or update the user with validated data. Set the password and save the user.
#         """
#         email = validated_data.get('email')
#         username = validated_data.get('username')
#         password = validated_data.get('password')

#         # Check if the user already exists
#         existing_user = CustomUser.objects.filter(email=email).first()
#         if existing_user:
#             # If user exists and password is missing, update the password
#             if not existing_user.password and password:
#                 existing_user.set_password(password)
#                 existing_user.save()
#                 return existing_user
#             elif existing_user.password:
#                 # If user exists with a password, return the existing user
#                 return existing_user
#         else:
#             # If user doesn't exist, create a new user
#             user = CustomUser(
#                 email=email,
#                 username=username,
#             )
#             user.set_password(password)
#             user.save()
#             return user
class PasswordUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['password']


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email']  

class AppointmentSerializer(serializers.ModelSerializer):
    # assigned_user = CustomUserSerializer(read_only=True) 
    user = CustomUserSerializer(read_only=True)  
    
    class Meta:
        model = Appointment
        # fields = ['id', 'appointment_title', 'start_date', 'start_time', 'end_time', 'assigned_user', 'created_at', 'user']
        fields='__all__'
    

