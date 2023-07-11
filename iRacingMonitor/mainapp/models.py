from django.db import models

# Create your models here.
class Member(models.Model):
  customer_id = models.IntegerField()    
  name = models.CharField(max_length=255)

class MetaInfo(models.Model):
  heading_color = models.CharField(max_length=255)
  data_color = models.CharField(max_length=255)
  total_color = models.CharField(max_length=255)
  name_color = models.CharField(max_length=255)
  heading_font = models.CharField(max_length=255)
  data_font = models.CharField(max_length=255)
  total_font = models.CharField(max_length=255)
  name_font = models.CharField(max_length=255)           
  
