from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .serializers import SignupSerializer, LoginSerializer, AppointmentSerializer
from rest_framework import status
from .models import CustomUser
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated


# Create your views here.


class UserLoginView(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = LoginSerializer(data=data)
            if serializer.is_valid():
                email = serializer.data["email"]
                password = serializer.data["password"]
                print("email", email)
                user = authenticate(email=email, password=password)

                if user is None:
                    return Response(
                        {
                            "status": 400,
                            "message": "Invalid credentials ",
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                refresh = RefreshToken.for_user(user)
                refresh["email"] = user.email

                data = {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "username":user.username,
                    "email":user.email
                }
                response_data = data
              

                return Response(response_data, status=status.HTTP_200_OK)

            else:
                return Response(
                    {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "Invalid data provided.",
                        "errors": serializer.errors,
                    }
                )

        except Exception as e:
            print(e)
            return Response(
                {
                    "status": 400,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserSignupAPI(APIView):
    def post(self, request):
        print("request.data", request.data)
        try:
            serializer = SignupSerializer(data=request.data)
            if serializer.is_valid():
                user_data = serializer.validated_data

                print(user_data, "ser_data")
                user = CustomUser(
                    email=user_data["email"],
                    username=user_data["username"],
                )

                user.set_password(user_data["password"])
                user.save()

                return Response(
                    {"message": "Account created successfully."},
                    status=status.HTTP_201_CREATED,
                )
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {
                    "message": e,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class AppointmentCreateView(APIView):

    def post(self, request):
        try:
            data = request.data

            profile = CustomUser.objects.get(email=data["email"])

            if not isinstance(profile, CustomUser):
                return Response(
                    {"error": "User is not a valid CustomUser."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            assigned_user = None
            if "assigned_user" in data:
                try:
                    assigned_user = CustomUser.objects.get(email=data["assigned_user"])
                except CustomUser.DoesNotExist:
                    return Response(
                        {"error": "Assigned user does not exist"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            # Create Appointment
            appointment = Appointment.objects.create(
                user=profile,
                appointment_title=data["appointment_title"],
                start_date=data["start_date"],
                start_time=data["start_time"],
                end_time=data.get("end_time"),
                assigned_user=assigned_user,
            )
            serializer = AppointmentSerializer(appointment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

class Getappointments(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user_id = request.query_params.get('id')
            user=CustomUser.objects.get(id=user_id) 
            appointments = user.appointments.all()
            appointment_serializer = AppointmentSerializer(appointments,many=True)
            response_data =  appointment_serializer.data

            return Response(response_data, status=status.HTTP_200_OK)
            

        except Exception as e:
            return Response(str(e), status=status.HTTP_200_OK)
# class Getappointmentdata(APIView):
#     def post(self,request):
#         try:
#             print("apiwebhook")
#             data=request.data
#             user, created = CustomUser.objects.get_or_create(email=data.get('email'),username=data.get('username'))
            
#             assigned_user = None
                
#             assigned_user = CustomUser.objects.get_or_create(username=data["assigned_user"])
              
#             # Create Appointment
#             appointment = Appointment.objects.create(
#                 user=user,
#                 appointment_location=data["appointment_location"],
#                 start_date=data["start_date"],
#                 start_time=data["start_time"],
#                 end_time=data.get("end_time"),
#                 assigned_user=assigned_user,
#                 tatto_idea=data.get('tatto_idea'),
#                 # reference_image=data.get('reference_Images')
#             )
#             serializer = AppointmentSerializer(appointment)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)

#         except Exception as e:
#             return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
#             print(request.data,"jjjjjjjjjjjjjjjjjjjjjjj")
#             return Response( status=status.HTTP_200_OK)
            

#         except Exception as e:
#             return Response(str(e), status=status.HTTP_200_OK)


class Getappointmentdata(APIView):
    def post(self, request):
        try:
            print("API Webhook called")
            data = request.data

            # Get or create the user
            user, created = CustomUser.objects.get_or_create(
             email=data.get('email'),
                defaults={'username': data.get('username')}
                )

            if not created:
                print(f"User with email {data.get('email')} already exists.")
            # Get or create the assigned user
            assigned_user, _ = CustomUser.objects.get_or_create(
                username=data.get("assigned_user")
            )
            overlapping_appointments = Appointment.objects.filter(
                user=user,
                start_date=data["start_date"],
                start_time__lt=data["end_time"],  # Start time is before the new appointment's end time
                end_time__gt=data["start_time"]   # End time is after the new appointment's start time
            )

            if overlapping_appointments.exists():
                return Response({"message": "Appointment time overlaps with an existing appointment."}, status=status.HTTP_400_BAD_REQUEST)
            
            
            # Create the appointment
            appointment = Appointment.objects.create(
                user=user,
                appointment_location=data["appointment_location"],
                start_date=data["start_date"],
                start_time=data["start_time"],
                end_time=data.get("end_time"),
                assigned_user=assigned_user,
                tatto_idea=data.get('tatto_idea'),
                # Uncomment and handle the reference image field if needed
                reference_image=data.get('reference_image')
            )

            # Serialize the created appointment
            serializer = AppointmentSerializer(appointment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except KeyError as e:
            # Handle missing required keys
            return Response(
                {"error": f"Missing required field: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            # Log exception and return error response
            print(f"Error occurred: {str(e)}")
            return Response(
                {"error": str(e),"An error occurred while creating the appointment."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
