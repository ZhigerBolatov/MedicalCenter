from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import HappyLifeUserManager


# Create your models here.

class Role(models.Model):
    name = models.CharField(max_length=255)

class Category(models.Model):
    name = models.CharField(max_length=255)

class HappyLifeUsers(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    # Password is included in own Django Users
    telephone = models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=255, unique=True)
    IIN = models.CharField(max_length=255, unique=True)
    user_address = models.TextField()
    category_id = models.ForeignKey('Category', blank=True, null=True, on_delete=models.SET_NULL)
    role_id = models.ForeignKey('Role', null=True, on_delete=models.SET_NULL)
    schedule_ids = models.ManyToManyField('Schedule', blank=True, null=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'IIN'
    REQUIRED_FIELDS = []
    object = HappyLifeUserManager()

class Schedule(models.Model):
    day = models.ForeignKey('Days', blank=True, null=True, on_delete=models.SET_NULL)
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()

class Parking(models.Model):
    user_id = models.ForeignKey('HappyLifeUsers', blank=True, null=True, on_delete=models.SET_NULL)
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()
    total = models.PositiveIntegerField()
    price = models.PositiveIntegerField()

class Days(models.Model):
    day = models.CharField(max_length=255, unique=True)

class Status(models.Model):
    status = models.CharField(max_length=255, unique=True)

class Booking(models.Model):
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()
    day = models.ForeignKey('Days', blank=True, null=True, on_delete=models.SET_NULL)
    status_id = models.ForeignKey('Status', blank=True, null=True, on_delete=models.SET_NULL)
    patient_id = models.ForeignKey('HappyLifeUsers', blank=True, null=True, on_delete=models.SET_NULL,
                                   related_name='booking_patient')
    doctor_id = models.ForeignKey('HappyLifeUsers', blank=True, null=True, on_delete=models.SET_NULL,
                                  related_name='booking_doctor')
    description = models.TextField()
    price = models.PositiveIntegerField()
