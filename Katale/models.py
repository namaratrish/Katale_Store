from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Users(models.Model):
    user = models.OneToOneField(User)
    city = models.CharField(max_length=30)
    address = models.CharField(max_length=30)
    birthdate = models.DateField()
    phone_number = models.PositiveIntegerField(max_length=15, null=False, blank=False)

    class Meta:
        db_table = "Users"

    def __unicode__(self):
        return self.user.username


class Category(models.Model):
    category = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'categories'
        ordering = ['-created_at']
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        return self.category


class Product(models.Model):
    product_name = models.CharField(max_length=30)
    description = models.TextField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    image = models.ImageField(upload_to='images', max_length=50)
    category = models.ForeignKey(Category, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'Products'

    def __unicode__(self):
        return self.product_name



