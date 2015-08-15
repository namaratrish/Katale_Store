from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Users(models.Model):
    user = models.OneToOneField(User)
    city = models.CharField(max_length=30)
    address = models.CharField(max_length=30)
    birthdate = models.DateField()
    phone_number = models.PositiveIntegerField(max_length=15)

    class Meta:
        db_table = "Users"

    def __unicode__(self):
        return self.user.username


class Product(models.Model):
    product_name = models.CharField(max_length=30)
    description = models.TextField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    image = models.ImageField(upload_to='images', max_length=50)

    class Meta:
        db_table = 'Products'

    def __unicode__(self):
        return self.product_name

