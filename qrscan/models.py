from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import CharField



class Tickett(models.Model):
    name=models.CharField(max_length=20)
    city=models.CharField(max_length=20)
    monument=models.CharField(max_length=20)
    date=models.DateField()
    email=models.EmailField()
    count=models.IntegerField()
    ticket_price=models.DecimalField(decimal_places=1,max_digits=7)
    total_cost=models.CharField(max_length=20)
    order_id = models.CharField(max_length=100, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True)
    paid = models.BooleanField(default=False)
    timevalid=models.DateTimeField(blank=True, null=True)
    verified=models.BooleanField(default=False)
    def __str__(self):
        if self.paid:
            a="paid"
        else:
            a="unpaid"
        if self.verified:
            b="verified"
        else:
            b="unverified"
        return f"{self.name}-{a}-{b}"

class MonumentTickets(models.Model):
    name=models.CharField(max_length=20)
    city=models.CharField(max_length=20)
    monument=models.CharField(max_length=20) #change max_length = 50
    date=models.DateField()
    email=models.EmailField()
    phone=models.IntegerField(max_length=10) #change max_length 
    
    count_adult=models.IntegerField()
    count_children=models.IntegerField()
    count_abroad=models.IntegerField()
    
    price_adult=models.DecimalField(decimal_places=1,max_digits=7)
    price_children=models.DecimalField(decimal_places=1,max_digits=7)
    price_abroad=models.DecimalField(decimal_places=1,max_digits=7)
    
    total_cost=models.CharField(max_length=20)
    order_id = models.CharField(max_length=100, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True)
    paid = models.BooleanField(default=False)
    timevalid=models.DateTimeField(blank=True, null=True)
    verified=models.BooleanField(default=False)

    total_count=models.IntegerField()

    def __str__(self):
        if self.paid:
            a="paid"
        else:
            a="unpaid"
        if self.verified:
            b="verified"
        else:
            b="unverified"
        return f"{self.name}-{a}-{b}"

class MonumentTickets(models.Model):
    name=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    monument=models.CharField(max_length=100) #change max_length = 50
    date=models.DateField()
    email=models.EmailField()
    phone=models.IntegerField(max_length=10) #change max_length 
    
    count_adult=models.IntegerField()
    count_children=models.IntegerField()
    count_abroad=models.IntegerField()
    
    price_adult=models.DecimalField(decimal_places=1,max_digits=7)
    price_children=models.DecimalField(decimal_places=1,max_digits=7)
    price_abroad=models.DecimalField(decimal_places=1,max_digits=7)
    
    total_cost=models.CharField(max_length=20)
    order_id = models.CharField(max_length=100, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True)
    paid = models.BooleanField(default=False)
    timevalid=models.DateTimeField(blank=True, null=True)
    verified=models.BooleanField(default=False)

    total_count=models.IntegerField()
    doc_type=models.CharField(max_length=20)
    personal_id_no=models.CharField(max_length=30)

    def __str__(self):
        if self.paid:
            a="paid"
        else:
            a="unpaid"
        if self.verified:
            b="verified"
        else:
            b="unverified"
        return f"{self.name}-{a}-{b}"