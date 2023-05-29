from django.db import connection, models

# Create your models here.

class Customers(models.Model):
    # def order_value():
    #     number = Customers.objects.order_by('-index').first()
    #     return number.index + 1 if number else 1
    customerid = models.CharField(max_length=40,blank=False, default='',primary_key=True)
    # index = models.IntegerField()
    firstname = models.TextField(default='')
    lastname = models.TextField(default='')
    company = models.CharField(max_length=40, default='')
    city = models.CharField(max_length=40, default='')
    country = models.CharField(max_length=100,default='')
    phone1 = models.CharField(max_length=50,default='')
    phone2 = models.CharField(max_length=50, default='')
    email = models.TextField(default='')
    subscriptiondate = models.DateField( default='')
    website = models.CharField(max_length=100,default='')
    filename_index = models.CharField(max_length=100, default='')
    