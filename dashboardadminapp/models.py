
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
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    middle_initial = models.CharField(max_length=5, blank=True, null=True)
    user_number = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=255, default="Avicast123")
    is_archived = models.BooleanField(default=False)  # ✅ Archive feature

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"


