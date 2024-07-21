from django.contrib import admin
from .models import TrackingNumber, Courier, TrackingState, DeliveryType, Statistic, UserActivity
# Register your models here.
 
# Registers inside the admin panel
admin.site.register(TrackingNumber)
admin.site.register(Courier)
admin.site.register(TrackingState)
admin.site.register(DeliveryType)
admin.site.register(Statistic)
admin.site.register(UserActivity)