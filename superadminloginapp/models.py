from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, ID_number, password=None):
        if not ID_number:
            raise ValueError("Users must have an ID number")
        user = self.model(ID_number=ID_number)
        user.set_password(password)  # Hashes the password
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    ID_number = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=128)

    objects = UserManager()

    USERNAME_FIELD = 'ID_number'

