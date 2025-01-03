from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path
from .views import *


urlpatterns = [
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/',UserSignupAPI.as_view()),
    path('admin-signup/',UseradminSignupAPI.as_view()),
    path('admin-login/', AdminsLoginAPI.as_view(), name='admin-login'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLOgOut.as_view(), name='logout'),
    path('create-appointment/',AppointmentCreateView.as_view(),name='createappointment'),
    path('get-appointments/',Getappointments.as_view(),name='getappointments'),
    path('get-formdata-appointment/',Getappointmentdata.as_view(),name='getappointmentdata'),
    path('get-registred-users/',Getregistreduser.as_view(),name='getuserslist'),
    path('remove-registred-users/',Removefromuserlist.as_view(),name='removeregistreduser'),
    
    path('createtoken-onboarding/', CreateAccessToken.as_view(), name='create_token'),
    path('get-customfield/', CustomfieldUpdation.as_view(), name='getcustomfield'),
    path('get-appointmentcount-filter/', GetBookingCountsLastWeekMonth.as_view(), name='getappointmentfilter'),
    path('reschedule-appointment-session/', RescheduleAppointmentSession.as_view(), name='getappointmentfilter'),
    path('get-available-slot/', AvailableSlotsAPI.as_view(), name='get-available-slot'),
        path('get-upcomming-appointments/', GetUpcomingAppointments.as_view(), name='get-upcommingappointments'),






    
]



