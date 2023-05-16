from django.db import models

# Create your models here.

class Customers(models.Model):
    customerid = models.CharField(max_length=40,blank=False, default='')
    firstname = models.TextField(blank=True, default='')
    lastname = models.TextField(blank=False, default='')
    company = models.CharField(max_length=40,blank=False, default='')
    city = models.CharField(max_length=40,blank=False, default='')
    country = models.CharField(max_length=100,blank=False, default='')
    phone1 = models.CharField(max_length=50,blank=False, default='')
    phone2 = models.CharField(max_length=50,blank=False, default='')
    email = models.TextField(blank=False, default='')
    subscriptiondate = models.DateField(blank=False, default='')
    website = models.CharField(max_length=100,blank=False, default='')
    cleanedphone1 = models.CharField(max_length=50,blank=False, default='')
    cleanedphone2 = models.CharField(max_length=50,blank=False, default='')
