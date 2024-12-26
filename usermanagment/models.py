from django.db import models

# Create your models here.
   
from django.db import models
from django.contrib.auth.models import AbstractUser



class CustomUser(AbstractUser):
   
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=False)
    appointmentbooked=models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = ['username']
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='userdata_groups',  # Custom reverse relation name
        blank=True
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='userdata_permissions',  # Custom reverse relation name
        blank=True
    )
    
    def _str_(self): 
        return  self.email 
       

class Appointment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='appointments')
    appointment_title = models.CharField(max_length=60,null=True)
    start_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(null=True, blank=True)
    assigned_user = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_appointments'
    )
    # assigned_user=models.CharField(max_length=50,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    appointment_location = models.CharField(max_length=100,null=True)  
    tatto_idea = models.CharField(max_length=255,null=True)  
    reference_image = models.ImageField(null=True, blank=True, upload_to='reference_images/')

    

    def __str__(self):
        return f"Appointment for {self.user.email} on {self.start_date}"
 
    