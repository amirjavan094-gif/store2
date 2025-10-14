from django.db import models
import datetime 
from django.contrib.auth.models import User
from django.db.models.signals import post_save



class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    

    

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User,auto_now=True)
    phone = models.CharField(max_length=25,blank=True)
    address1 = models.CharField(max_length=250,blank=True)
    address2 = models.CharField(max_length=250,blank=True)
    city = models.CharField(max_length=25,blank=True)
    state = models.CharField(max_length=25,blank=True)
    zipcode = models.CharField(max_length=25,blank=True)
    country =models.CharField(max_length=25,default='iran')
    old_cart =models.CharField(max_length=20,blank=True,null=True)


    def __str__(self):
        return self.user.username
    

def createprofile(sender, instance, created, **kwargs):
    if created :
        user_profile = Profile(user=instance)
        user_profile.save()

post_save.connect(createprofile,sender=User)



    

class Products(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=500, default='', blank=True, null=True)
    price = models.DecimalField(default=0, decimal_places=0, max_digits=12)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1,related_name="products")
    picture = models.ImageField(upload_to='upload/product/')
    exist = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    

