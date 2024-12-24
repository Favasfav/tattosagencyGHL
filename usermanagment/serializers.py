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
    

