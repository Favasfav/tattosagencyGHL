from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .serializers import SignupSerializer, LoginSerializer, AppointmentSerializer,CustomUserSerializer
from rest_framework import status
from .models import CustomUser
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from datetime import datetime
from django.db import transaction
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
                    # "username":user.username,
                    # "email":user.email,
                    # "id":user.id
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


# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.contrib.auth import authenticate
# from rest_framework_simplejwt.tokens import RefreshToken
# from .serializers import LoginSerializer

# class UserLoginView(APIView):
#     def post(self, request):
#         try:
#             data = request.data
#             serializer = LoginSerializer(data=data)
#             if serializer.is_valid():
#                 email = serializer.data["email"]
#                 password = serializer.data["password"]
#                 print("email", email)
#                 user = authenticate(email=email, password=password)

#                 if user is None:
#                     response = Response(
#                         {
#                             "status": 400,
#                             "message": "Invalid credentials ",
#                         },
#                         status=status.HTTP_400_BAD_REQUEST,
#                     )

#                     response.delete_cookie('jwt')  
#                     return response

#                 refresh = RefreshToken.for_user(user)
#                 refresh["email"] = user.email

#                 response = Response({"success": "Logged in successfully"})

#                 response.set_cookie(
#                     key='jwt', 
#                     value=str(refresh.access_token), 
#                     httponly=True, 
#                     secure=True,  
#                     samesite='Lax',
#                 )

#                 return response 

#             else:
               
#                 response.delete_cookie('jwt')  

#                 return Response(
#                     {
#                         "status": status.HTTP_400_BAD_REQUEST,
#                         "message": "Invalid data provided.",
#                         "errors": serializer.errors,
#                     }
#                 )

#         except Exception as e:
#             print(e)
#             return Response(
#                 {
#                     "status": 400,
#                 },
#                 status=status.HTTP_400_BAD_REQUEST,
#             )




class UserSignupAPI(APIView):
    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')

            existing_user = CustomUser.objects.filter(email=email).first()

            if existing_user:
                if not existing_user.password:
                    existing_user.set_password(password)
                    existing_user.save()
                    return Response(
                        {"message": "Password set successfully for existing user."},
                        status=status.HTTP_200_OK
                    )
                return Response(
                    {"message": "User already exists."},
                    status=status.HTTP_200_OK
                )

            serializer = SignupSerializer(data=request.data)
            if serializer.is_valid():
                user_data = serializer.validated_data
                username = user_data.get('username')

                user = CustomUser(email=email, username=username,registreduser=True)
                user.set_password(password)
                user.save()

                return Response(
                    {"message": "Account created successfully."},
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except CustomUser.DoesNotExist:
            return Response(
                {"message": "User does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"message": str(e)},
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
            assigned_user_id = request.query_params.get('id')
            user=CustomUser.objects.get(id=assigned_user_id) 
            appointments = user.assigned_appointments.all()
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


# 




class Getappointmentdata(APIView):
    @transaction.atomic
    def post(self, request):
        try:
            print("API Webhook called", request.data)
            
            # Extract the 'customData' from the request data
            data = request.data
            custom_data = data.get('customData', {})
            
            username = custom_data.get('username', None) 
            email = custom_data.get('email', None)  
            appointment_location = custom_data.get('appointment_location', None)  
            start_time = custom_data.get('start_time', None)  
            end_time = custom_data.get('end_time', None)  
            start_date = custom_data.get('start_date', None) 
            tattoo_idea = custom_data.get('tatto_idea', None)  
            reference_images = custom_data.get('reference_Images', None)  
            assigned_username = custom_data.get('assigned_user', None)  

            # print(f"username: {username}")
            # print(f"email: {email}")
            # print(f"appointment_location: {appointment_location}")
            # print(f"start_time: {start_time}")
            # print(f"end_time: {end_time}")
            # print(f"start_date: {start_date}")
            # print(f"tatto_idea: {tattoo_idea}")
            # print(f"reference_images: {reference_images}")
            # print(f"assigned_user: {assigned_user}")
            start_time = datetime.strptime(start_time, '%I:%M %p').time()
            end_time = datetime.strptime(end_time, '%I:%M %p').time()

            user, created = CustomUser.objects.get_or_create(email=email,defaults={'username':username})
            
            
            
            overlapping_appointments = Appointment.objects.filter(
            user=user,
            start_date=start_date,).filter(
            Q(start_time__lt=end_time, end_time__gt=start_time)  
            
            )

            if overlapping_appointments.exists():
                return Response({"message": "Appointment time overlaps with an existing appointment."}, status=status.HTTP_400_BAD_REQUEST)

            # assigned_user, created = CustomUser.objects.get_or_create(username=assigned_username,defaults={"email":assigned_username})
            try:
                    assigned_user = CustomUser.objects.get(username=assigned_username)
            except ObjectDoesNotExist:
                return Response(
                     {"error": f"Assigned user does not exist: {assigned_username}"},
                     status=status.HTTP_400_BAD_REQUEST
                     )
            print('assigned user',assigned_user.__dict__)
            # raise Exception 
            appointment = Appointment.objects.create(
                user=user,
                appointment_location=appointment_location,
                start_date=start_date,
                start_time=start_time,
                end_time=end_time,
                assigned_user=assigned_user,
                tatto_idea=tattoo_idea,
                reference_image=reference_images
            )
            if appointment:
                user.appointmentbooked=True
            serializer = AppointmentSerializer(appointment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except KeyError as e:
            return Response(
                {"error": f"Missing required field: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )




class Getregistreduser(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # user_id = request.query_params.get('id')
            users=CustomUser.objects.filter(registreduser=True) 
            # appointments = Appointment.appointments.all()
            # user_ids = Appointment.objects.values('user_id').distinct()
            # users = CustomUser.objects.filter(id__in=user_ids)
            user_serializer = CustomUserSerializer(users,many=True)
            response_data =  user_serializer.data

            return Response(response_data, status=status.HTTP_200_OK)
            

        except Exception as e:
            return Response(str(e), status=status.HTTP_200_OK)


class Removefromuserlist(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            id =request.data.get('id')
            users = CustomUser.objects.get(id=id).delete()
            
            return Response({"message":"successfully removed"}, status=status.HTTP_200_OK)
            

        except Exception as e:
            return Response(str(e), status=status.HTTP_200_OK)