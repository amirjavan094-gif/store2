from django.db import models
from django.contrib.auth.models import User
from store.models import Products
from django.db.models.signals import post_save 
from django_jalali.db import models as jmodels
import jdatetime

class ShippingAddress(models.Model):
    user = models.ForeignKey(User,on_delete= models.CASCADE,null=True,blank=True) 
    shipping_full_name =models.CharField(max_length=250)
    shipping_email= models.EmailField(max_length=250,blank=True)
    shipping_phone = models.CharField(max_length=25,blank=True)
    shipping_address1 = models.CharField(max_length=250,blank=True)
    shipping_address2 = models.CharField(max_length=250,blank=True,null=True)
    shipping_city = models.CharField(max_length=25,blank=True)
    shipping_state = models.CharField(max_length=25,blank=True)
    shipping_zipcode = models.CharField(max_length=25,blank=True)
    shipping_country =models.CharField(max_length=25,default='iran')
    shipping_old_cart =models.CharField(max_length=20,blank=True,null=True)

    class Meta:
        verbose_name_plural = 'shiping address'

   
    def __str__(self):
        return f'shiping address from {self.shipping_full_name}'
    

def create_shipping_user(sender, instance, created, **kwargs):
    if created :
        user_shipping = ShippingAddress(user=instance)
        user_shipping.save()

post_save.connect(create_shipping_user,sender=User)
    


class Order(models.Model):
    STATUS_ORDER = [
        ("Pending","در انتظار پرداخت "),
        ("Processing","در حال پردازش  "),
        ("shipped","ارسال شده ب پست  "),
        ("Delivered","تحویل داده شده  ")
        
        
        
        ]
    user = models.ForeignKey(User,on_delete= models.CASCADE,null=True,blank=True)
    full_name = models.CharField(max_length=60)
    email=models.CharField(max_length=100,blank=True)
    shipping_address = models.TextField(max_length=1500000)
    amount_paid = models.DecimalField(decimal_places=0, max_digits=12)
    date_ordered = jmodels.jDateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,choices=STATUS_ORDER,default='Pending')
    last_update = jmodels.jDateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
    # اگر رکورد قبلاً وجود داشت، وضعیت قدیمی را بخوان و در صورت تغییر last_update را قرار بده
        if self.pk:
            try:
                old_status = Order.objects.get(pk=self.pk).status
            except Order.DoesNotExist:
                old_status = None

            if old_status != self.status:
                self.last_update = jdatetime.datetime.now()

    # همیشه رکورد را ذخیره کن (برای ایجاد یا بروزرسانی)
        super().save(*args, **kwargs)



    def __str__(self):
        return f"order {self.id}"
    


class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Products,on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)

    quantity = models.PositiveIntegerField(default=1,)
    price =  models.DecimalField(decimal_places=0, max_digits=12)


    def __str__(self):
        if self.user is not None:
          return f'order item {self.id} for {self.user}'
        else:
            return f'order item {self.id}'
    




