from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

def create_user_with_hashed_password(username, raw_password):
    """
    Example: Create a user with a securely hashed password using Django's utilities.
    """
    user = User(username=username)
    user.password = make_password(raw_password)  # password is hashed before saving
    user.save()
    return user