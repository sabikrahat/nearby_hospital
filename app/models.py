from django.db import models

# Create your models here.
class UserModel(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=40)
    password = models.CharField(max_length=1024)
    isAdmin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'app_users'

class UserContact(models.Model):
    messengerId = models.CharField(max_length=10)
    messengerName = models.CharField(max_length=50)
    messengerEmail = models.CharField(max_length=40)
    message = models.CharField(max_length=3072)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'app_users_contacts'

class hospitalModel(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    phone = models.CharField(max_length=15)
    email = models.CharField(max_length=40)
    services = models.CharField(max_length=255)
    departments = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'app_hospitals'

class doctorModel(models.Model):
    name = models.CharField(max_length=50)
    degrees = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    hospital = models.ForeignKey(hospitalModel, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    isSaturday = models.BooleanField(default=False)
    isSunday = models.BooleanField(default=False)
    isMonday = models.BooleanField(default=False)
    isTuesday = models.BooleanField(default=False)
    isWednesday = models.BooleanField(default=False)
    isThursday = models.BooleanField(default=False)
    isFriday = models.BooleanField(default=False)
    apointmentTime = models.CharField(max_length=100)
    availableTime = models.CharField(max_length=100)
    fees = models.CharField(max_length=50)
    rating = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'app_doctors'

class ambulanceModel(models.Model):
    name = models.CharField(max_length=50)
    hospital = models.ForeignKey(hospitalModel, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    phone = models.CharField(max_length=15)
    services = models.CharField(max_length=255)
    fees = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'app_ambulances'