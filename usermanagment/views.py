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
from datetime import datetime,timedelta
from django.db import transaction
from django.utils import timezone
import requests
from .models import Appointment
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
                try:
            #         "id": "AjUJ2bojgCd4zQBUCwPc",
            # "name": "Artists: All",
                        customField_id="uuU8QYKdKbuJauoEXjWB"
                        user_location_id="0rrNZinFkHbXD50u5nyq"
                        url = f"https://services.leadconnectorhq.com/locations/{user_location_id}/customFields/{customField_id}"
                        usernames = CustomUser.objects.all()
                        userlist=CustomUserSerializer(usernames,many=True).data 
                        username_list=[user['username'] for user in userlist]
                        print("usernames",userlist)
                        payload = {
                            "name": "Artists: All123",  
                            "model": "contact",      
                            "options":  username_list,
                            "position": 850,         
                            "dataType": "SINGLE_OPTIONS" 
                        }

                        # Headers
                        headers = {
                            "Authorization": f"Bearer {Authtable.objects.get(location_id=user_location_id).access_token}",
                            "Version": "2021-07-28",
                            "Content-Type": "application/json",
                            "Accept": "application/json"
                        }

                        response = requests.put(url, json=payload, headers=headers)
                except Exception as e:
                    
                        return Response(
                            {"message":  {str(e)}},
                            status=status.HTTP_400_BAD_REQUEST,
                        )

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
                # start_date=data["start_date"],
                # start_time=data["start_time"],
                # end_time=data.get("end_time"),
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
            print("customdata",custom_data)
            
            username = custom_data.get('username', None) 
            email = custom_data.get('email', None)  
            appointment_location = custom_data.get('appointment_location', None)  
            # start_time = custom_data.get('start_time', None)  
            # end_time = custom_data.get('end_time', None)  
            # start_date = custom_data.get('start_date', None) 
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
            
            try:
                    assigned_user = CustomUser.objects.get(username=assigned_username)
            except ObjectDoesNotExist:
                return Response(
                     {"error": f"Assigned user does not exist: {assigned_username}"},
                     status=status.HTTP_400_BAD_REQUEST
                     )
            
            print("assssss",assigned_user,user,Appointment)
            # overlapping_appointments = Appointment.objects.filter(assigned_user=assigned_user,start_date=start_date,).filter(
            # Q(start_time__lt=end_time, end_time__gt=start_time)  
            
            # )

            if overlapping_appointments.exists():
                return Response({"message": "Appointment time overlaps with an existing appointment."}, status=status.HTTP_400_BAD_REQUEST)

            # assigned_user, created = CustomUser.objects.get_or_create(username=assigned_username,defaults={"email":assigned_username})
            
            print('assigned user',assigned_user.__dict__)
            # raise Exception 
            # appointment = Appointment.objects.create(
            #     user=user,
            #     appointment_location=appointment_location,
            #     # start_date=start_date,
            #     # start_time=start_time,
            #     # end_time=end_time,
            #     assigned_user=assigned_user,
            #     tatto_idea=tattoo_idea,
            #     reference_image=reference_images
            # )
           
            # serializer = AppointmentSerializer(appointment)
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response( status=status.HTTP_201_CREATED)


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
    permission_classes = [IsAuthenticated]

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








class CreateAccessToken(APIView):
    def post(self,request):
        try:
            user_location_id = request.data['location_id']
            code = request.data.get('code')
            if not user_location_id or not code:
                raise ValidationError("location_id and code are required fields.")
            
            access_token_instance = Authtable.objects.get(location_id=user_location_id)
            if access_token_instance:  
                print("access token exists")
                url ="https://services.leadconnectorhq.com/oauth/token"  
                
                payload = {
                    "client_id": "676ea0af5376ec6a434adb0f-m56qun8a",
                    "client_secret": "8528d5d0-147b-4da1-865f-be8f5d5b98ff",
                    "grant_type": "refresh_token",
                    "code": code,
                    "user_type": "Location",
                    "refresh_token" : access_token_instance.refresh_token ,
                    
                }
            
                headers = {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Accept": "application/json"
                }

                response = requests.post(url, data=payload, headers=headers)
            
                if response.ok:
                
                    access_token = response.json()['access_token']
                    refresh_token = response.json()['refresh_token']
                    expires_in = timezone.now() + timedelta(seconds=response.json()['expires_in'])

                    response_location_id = response.json()['locationId']

                    if response_location_id == user_location_id:
                       
                        access_token_instance.access_token = access_token
                        access_token_instance.refresh_token = refresh_token
                        access_token_instance.expires_in = expires_in         
                    
                        access_token_instance.save()

                        return Response({'message':  "Successfully created access token","data":response.json()},status=200)

                    else:
                        return Response({'message': "Wrong Location Id"},status=400)
                    
                else:
                    print(response.text)
                    return Response({'message1': response.text},status=response.status_code) 
            
        except Authtable.DoesNotExist:
            print("doesnot exist")
            url ="https://services.leadconnectorhq.com/oauth/token"  
            
            payload = {
                "client_id": "676ea0af5376ec6a434adb0f-m56qun8a",
                "client_secret": "8528d5d0-147b-4da1-865f-be8f5d5b98ff",
                "grant_type": "authorization_code",
                "code": code,
                "user_type": "Location",
                
            }
        
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json"
            }

            response = requests.post(url, data=payload, headers=headers)
        
            if response.ok:
            
                access_token = response.json()['access_token']
                refresh_token = response.json()['refresh_token']
                expiry_time = timezone.now() + timedelta(seconds=response.json()['expires_in'])

               
                response_location_id = response.json()['locationId']

                if response_location_id == user_location_id:
                             
                    instance = Authtable.objects.create(
                        location_id=response_location_id,
                        access_token=access_token,
                        refresh_token=refresh_token,
                        expires_in=expiry_time,
                    )
                  
                    instance.save()

                    return Response({'message':  "Successfully created access token"},status=200)

                else:
                    return Response({'message': "Wrong Location Id"},status=400)
                
            else:
                print(response.text)
                return Response({'message': response.text},status=response.status_code)

        except Exception as e:
            print(e)
            return Response({'message3': str(e)}, status=500)



class Appointmentonboarding(APIView):
    def get(self,request):
        try:
            user_location_id = request.data['location_id']
            contact_id=request.data['contact_id']
        
            print(user_location_id)
            url = f"https://services.leadconnectorhq.com/contacts/{contact_id}/appointments"


            headers = {
                "Authorization": f"Bearer {Authtable.objects.get(location_id=user_location_id).access_token}",
                "Version": "2021-07-28",
                "Accept": "application/json"
            }

            response = requests.get(url, headers=headers)

            print(contact_id)

            url1 = f"https://services.leadconnectorhq.com/contacts/{contact_id}"
            response1= requests.get(url1,headers=headers)
            combined_data = {
                "appointments": response,
                "contact_details": response1
            }

            return Response(combined_data,status=status.HTTP_200_OK) 
        except Exception as e:
            
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)
        


class CustomfieldUpdation(APIView):
        def get(self,request):
            try:
                user_location_id = request.query_params.get('location_id')
                customField_id=request.query_params.get('customField_id')
            
                if not user_location_id or  not customField_id:

                    return Response({"message":"invalid location_id or contact_id "},status=status.HTTP_200_OK)
                url = f"https://services.leadconnectorhq.com/locations/{user_location_id}/customFields/{customField_id}"

                headers = {
                    "Authorization": f"Bearer {Authtable.objects.get(location_id=user_location_id).access_token}",
                    "Version": "2021-07-28",
                    "Accept": "application/json"
                }

                response = requests.get(url, headers=headers)

                print(response.json())
                return Response(response.json(),status=status.HTTP_200_OK) 
            except Exception as e:
                return Response(str(e),status=status.HTTP_400_BAD_REQUEST)



        def put(self,request):
            try:
                user_location_id = request.data.get('location_id')
                customField_id=request.data.get('customField_id')
            
                if not user_location_id or  not customField_id:

                    return Response({"message":"invalid location_id or contact_id "},status=status.HTTP_200_OK)
                

                url = f"https://services.leadconnectorhq.com/locations/{user_location_id}/customFields/{customField_id}"
                usernames = CustomUser.objects.all()
                userlist=CustomUserSerializer(usernames,many=True).data 
                username_list=[user['username'] for user in userlist]
                print("usernames",userlist)
                # Updated payload
                payload = {
                    "name": "Artists: All123",  
                    "model": "contact",      
                    "options":  username_list[:10],
                    "position": 850,         
                    "dataType": "SINGLE_OPTIONS" 
                }

                # Headers
                headers = {
                    "Authorization": f"Bearer {Authtable.objects.get(location_id=user_location_id).access_token}",
                    "Version": "2021-07-28",
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                }

                # Make the PUT request
                response = requests.put(url, json=payload, headers=headers)

                # Print the response
                print(response.json())

                return Response(response.json(),status=status.HTTP_200_OK) 
            except Exception as e:
                return Response(str(e),status=status.HTTP_400_BAD_REQUEST)



