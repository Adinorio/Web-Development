from django.contrib.auth.backends import ModelBackend
from .models import User  # Ensure this matches your User model import

class IDNumberAuthBackend(ModelBackend):
    def authenticate(self, request, ID_number=None, password=None, **kwargs):
        try:
            user = User.objects.get(ID_number=ID_number)  # Look up user by ID_number
            if user.check_password(password):  # Verify hashed password
                return user
        except User.DoesNotExist:
            return None
