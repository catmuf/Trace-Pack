from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# changes standard python class to django model
class Courier(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=50)
    website = models.CharField(max_length=100, null=True)

    # String representation of the table Courier
    def __str__(self):
        return self.name
    
class DeliveryType(models.Model):
    delivery_type = models.CharField(max_length=20, null=True, blank=False)

    def __str__(self):
        return self.delivery_type
    
class TrackingNumber(models.Model):
    # Charfield by default blank is true
    title = models.CharField(max_length=100, null=True, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    tracking_number = models.CharField(max_length=50)
    delivery_type = models.ForeignKey(DeliveryType, on_delete=models.CASCADE, null=True, blank=False)
    origin_country_code = models.CharField(max_length=10, null=True, blank=True)
    destination_country_code = models.CharField(max_length=10, null=True, blank=True)
    courier_selected = models.CharField(max_length=50, null=True, blank=True)
    couriers_involved = models.ManyToManyField(Courier, related_name='participants', blank=True)
    status_milestone = models.CharField(max_length=50, null=True, blank=True)
    # db can leave null and blank for form as empty
    # status = models.TextField(null=True, blank=True)
    estimated_delivery_date = models.DateTimeField(null=True, blank=True)
    # Timestamps every modification
    updated = models.DateTimeField(auto_now=True)
    # Timestamps once the creation
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        # DESC order
        ordering = ['-updated']

    def __str__(self):
        return str(self.id) + " - " + self.user.username + " - " + self.title + " - " + self.tracking_number
    
class TrackingState(models.Model):
    tracking_number = models.ForeignKey(TrackingNumber, on_delete=models.CASCADE)
    event_tracking_number = models.CharField(max_length=50, null=True)
    status = models.TextField(null=True, blank=True)
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE, null=True, blank=True)
    occurrence_date_time = models.DateTimeField(null=True)
    status_milestone = models.CharField(max_length=50, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return self.tracking_number.tracking_number + " - " + str(self.occurrence_date_time)
    
class Statistic(models.Model):
    tracking_number = models.ForeignKey(TrackingNumber, on_delete=models.CASCADE)
    info_received_date_time = models.DateTimeField(null=True, blank=True)
    in_transit_date_time = models.DateTimeField(null=True, blank=True)
    outFor_delivery_date_time = models.DateTimeField(null=True, blank=True)
    failed_attempt_date_time = models.DateTimeField(null=True, blank=True)
    available_for_pickup_date_time = models.DateTimeField(null=True, blank=True)
    exception_date_time = models.DateTimeField(null=True, blank=True)
    delivered_date_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.id) + " - " + self.tracking_number
    
class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ip_address = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=255)
    modification = models.TextField(max_length=255, null=True)
    url = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'User Activities'

    def __str__(self):
        return str(self.user.username) + ' - ' + str(self.timestamp) + ' - ' + self.url