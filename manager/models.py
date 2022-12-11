from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    phnumber = models.CharField(max_length=12, null=False, blank=False)
    choices = (
        ('emp', 'employee'),
        ('ten', 'tenant'),
        ('adm', 'admin'),
    )
    user_type = models.CharField(max_length=3, choices=choices, default='ten', null=False, blank=False)
    apartment = models.ForeignKey('apartments', on_delete=models.CASCADE, null=True, blank=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} - {self.user_type}"

class apartments(models.Model):
    name = models.CharField(max_length=100, )
    contact = models.CharField(max_length=12, null=True, blank=True)
    apartment_desc = models.TextField()
    bhk = models.IntegerField(blank=False, null=False,default=1)
    location = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.bhk}"

class Utilities(models.Model):
    name = models.CharField(max_length=200,null=False, blank=False)
    description = models.TextField()
    price = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return f"{self.name}"

class Bookings(models.Model):
    util = models.ForeignKey(Utilities, on_delete=models.CASCADE, related_name="bookings")
    req_user = models.ForeignKey(User, limit_choices_to={'user_type': 'ten'}, on_delete=models.CASCADE, related_name="requests")
    assigned = models.ForeignKey(User, limit_choices_to={'user_type': 'emp'}, on_delete=models.CASCADE, related_name="jobs", null=True)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)

    class Meta:
        unique_together = ('req_user', 'util')

    def __str__(self):
        return f"{self.util} - {self.req_user} - {self.date}"

class Announcement(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    apartment = models.ForeignKey(apartments, on_delete=models.CASCADE, related_name="announcements")

    def __str__(self):
        return f"{self.title} - {self.apartment}"

class Tenantrequest(models.Model):
    apartment = models.ForeignKey(apartments, on_delete=models.CASCADE, related_name="tenrequests")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tenrequests")
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.apartment}"