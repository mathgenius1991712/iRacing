from django.core import validators
from django import forms
from django.contrib.auth import authenticate
from .models import CustomUser

def validate_login(request):
  email = request.POST["email"]
  password = request.POST["password"]
  try:
    validators.validate_email(email)
  except forms.ValidationError:
    message = "Invalid Email Address"
    return False, message
  if not CustomUser.objects.filter(email = email).exists():
    message = "Not Registered User"
    return False, message
  user = CustomUser.objects.filter(email = email).first()
  
  user = authenticate(email=email, password=password)
  if user is None:
    message = "Password is wrong"
    return False, message

  return True, "Validation Success"


