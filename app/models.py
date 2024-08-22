from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models.functions import Lower
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator

# Create your models here.

class Profile(models.Model):

    DEPARTMENT_CHOICES = [
        ('Admin', 'Admin'),
        ('Analyst', 'Analyst'),
        ('Compliance', 'Compliance'),
        ('Information Technology', 'Information Technology'),
        ('Marketing', 'Marketing')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    modified_date = models.DateTimeField(auto_now=True, editable=False)
    
    mobile_phone = models.CharField(max_length=20,
                                     null=True, 
                                     blank=True, 
                                     validators=[RegexValidator(regex='^\d{3}-\d{3}-\d{4}$', message='Please enter the mobile phone number in the following format: 999-999-9999.')], 
                                     verbose_name='Mobile Phone')
    office_phone = models.CharField(max_length=20, 
                                    null=True, 
                                    blank=True, 
                                    validators=[RegexValidator(regex='^\d{3}-\d{3}-\d{4}$', message='Please enter the office phone number in the following format: 999-999-9999.')],  
                                    verbose_name='Office Phone')
    phone_extension = models.CharField(max_length=5, 
                                       null=True, 
                                       blank=True, 
                                       validators=[RegexValidator(regex='^\d+$', message='Phone extension must be entered as digits only.')], 
                                       verbose_name='Phone Extension')
    address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=30, null=True, blank=True)
    state = models.CharField(max_length=2, null=True, blank=True, default='TX', error_messages="Enter the state's abbreviated name.")
    zip_code = models.CharField(max_length=5, 
                                null=True, 
                                blank=True, 
                                validators=[RegexValidator(regex='^\d+$', message='Zip code must be entered as digits only.')], 
                                verbose_name='Zip Code')
    last_four_ssn = models.CharField(max_length=4, 
                                     null=True, 
                                     blank=True, 
                                     validators=[RegexValidator(regex='^\d+$', message="Enter the last four digits of the user's SSN.")], 
                                     verbose_name='Last Four SSN')
    birthday = models.DateField(null=True, blank=True)
    personal_email = models.EmailField(null=True, blank=True, help_text = "Enter the user's personal email address.", verbose_name='Personal Email')
    
    ip_address = models.CharField(max_length=20, 
                                  null=True, 
                                  blank=True, 
                                  validators=[RegexValidator(regex='^\d{3}\.\d{3}\.\d{3}\.\d{3}$', message="IP field must match the following format: 111.111.111.111")], 
                                  verbose_name='IP Address',
                                  help_text="Enter the user's IP address. Use format 111.111.111.111")
    department = models.CharField(max_length=50, null=True, blank=True, choices=DEPARTMENT_CHOICES)
    bonus_rate = models.DecimalField(null=True, 
                                    blank=True, 
                                    decimal_places=2, 
                                    max_digits=3,
                                    validators=[MinValueValidator(limit_value=0, message='Bonus rate must be a positive number.'), MaxValueValidator(limit_value=1, message='Bonus rate must not exceed 1.0')],
                                    verbose_name='Bonus Rate', 
                                    help_text='Enter bonus rate as format "0.03" to represent 3%. This is the default rate for analysts.')
    offer_date = models.DateField(null=True, blank=True, verbose_name='Offer Date', help_text='Enter the date the offer letter was sent.')
    start_date = models.DateField(null=True, blank=True, verbose_name='Start Date', help_text='Enter the date the user started.')
    term_date = models.DateField(null=True, blank=True, verbose_name='Term Date', help_text="Enter the date the user's employment was terminated.")


    class Meta:
        db_table = 'auth_profile'

    def __str__(self):
        return self.user.username
    
@receiver(post_save, sender=User)
def create_or_update_user_tables(instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        AccessCredential.objects.create(user=instance)
    else:
        instance.profile.save()
        instance.accesscredential.save()



class AccessCredential(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    modified_date = models.DateTimeField(auto_now=True, editable=False)
    availity_id = models.CharField(max_length=50, null=True, blank=True, verbose_name='Availity ID', help_text="Enter the user's created Availity ID.")
    uhc_id = models.CharField(max_length=50, null=True, blank=True, verbose_name='United Healthcare ID', help_text="Enter the user's United Healthcare username.")
    jefferson_campus_key = models.CharField(max_length=50, null=True, blank=True, verbose_name='Campus Key', help_text="Enter the user's Jefferson/Einstein campus key.")
    trinity_id = models.CharField(max_length=50, null=True, blank=True, verbose_name='Trinity ID', help_text="Enter the user's Trinity Network ID.")

    class Meta:
        db_table = 'auth_access'

    def __str__(self):
        return self.user.username
    
class Film(models.Model):

    name = models.CharField(max_length=128, unique=True)
    users = models.ManyToManyField(User, related_name='films', through='UserFilms')
    photo = models.ImageField(upload_to='film_photos/', null=True, blank=True)
    
    class Meta:
        ordering = [Lower('name')]
        
class UserFilms(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField()
    
    class Meta:
        ordering = ['order']

