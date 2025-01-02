from django.db import models

# Create your models here.
   
from django.db import models
from django.contrib.auth.models import AbstractUser



class CustomUser(AbstractUser):
   
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=False)
    registreduser=models.BooleanField(default=False)
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
    
    def __str__(self):
        return  self.email 
       

class Appointment(models.Model):
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='appointments')
    appointment_title = models.CharField(max_length=60,null=True)
    # start_date = models.DateField()
    # start_time = models.TimeField()
    # end_time = models.TimeField(null=True, blank=True)
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

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'assigned_user', 'appointment_location'],
                name='unique_appointment_user_assigned_location'
            )
        ]

    def __str__(self):
        return f"Appointment for {self.user.email}"
 

class Session(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='sessions')
    start_time = models.TimeField()
    end_time = models.TimeField(null=True, blank=True)
    session_date = models.DateField()  # This captures the date for each session.    
    session_no = models.IntegerField( null=True, blank=True)
    def __str__(self):
        return f"Session on {self.session_date} from {self.start_time} to {self.end_time}"
from django.db import models

# Create your models here.this is for ghl auth token for updating custom field
class Authtable(models.Model):
    location_id=models.CharField(unique=True)
    access_token=models.CharField()
    refresh_token=models.CharField()
    expires_in =models.DateTimeField( auto_now_add=False)

    def __str__(self):
        return self.access_token()