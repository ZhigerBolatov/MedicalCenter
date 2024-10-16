from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register([Role, Category, HappyLifeUsers, Schedule, Parking, Days, Status, Booking])