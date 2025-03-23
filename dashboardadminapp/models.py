
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class SuperAdminUserManager(BaseUserManager):
    def create_user(self, user_number, password=None, **extra_fields):
        if not user_number:
            raise ValueError("The User Number is required")
        
        user = self.model(user_number=user_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class SuperAdminUser(models.Model):
    lastname = models.CharField(max_length=50)
    firstname = models.CharField(max_length=50)
    middle_initial = models.CharField(max_length=5, blank=True, null=True)
    user_number = models.CharField(max_length=20, unique=True)  # ✅ Year/001/random format
    password = models.CharField(max_length=255, default="Avicast123")  # ✅ Default password

    def __str__(self):
        return f"{self.lastname}, {self.firstname}"

