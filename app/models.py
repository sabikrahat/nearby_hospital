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