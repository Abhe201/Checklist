from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100, default="Default Location")

    def __str__(self):
        return f"{self.user.username} - {self.location}"

# Signal to create or update a Profile whenever a User is created or updated
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class Service(models.Model):
    serial = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, verbose_name="Service Name")
    category = models.CharField(max_length=200, null=True, blank=True, verbose_name="Category")
    ip = models.CharField(max_length=18, null=True, blank=True, verbose_name="IP Address")
    frequency = models.CharField(max_length=50, default="Daily")
    locations = models.ManyToManyField('Location', verbose_name="Locations")  # Updated for multiple locations

    STATUS_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
        ('N/A', 'N/A'),
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='N/A',
        verbose_name="Status"
    )
    remarks = models.TextField(blank=True, null=True, verbose_name="Remarks")

    def __str__(self):
        return f"{self.serial} - {self.name}"


class Location(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Location Name")

    def __str__(self):
        return self.name