from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/',UserSignupAPI.as_view()),
    path('login/', UserLoginView.as_view(), name='login'),
    path('create-appointment/',AppointmentCreateView.as_view(),name='createappointment'),
    path('get-appointments/',Getappointments.as_view(),name='getappointments'),
    path('get-formdata-appointment/',Getappointmentdata.as_view(),name='getappointmentdata'),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
