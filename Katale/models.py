from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Users(models.Model):
    user = models.OneToOneField(User)
    city = models.CharField(max_length=30)
    address = models.CharField(max_length=30)
    birthdate = models.DateField()
    phone_number = models.PositiveIntegerField(null=False, blank=False)

    class Meta:
        db_table = "Users"

    def __unicode__(self):
        return self.user.username


class Category(models.Model):
    category = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # parent = models.ForeignKey('self', blank=True, null=True, related_name='child')

    class Meta:
        db_table = 'categories'
        ordering = ['-created_at']
        verbose_name_plural = 'Categories'

    def category_name(self):
        return self.category

    def __unicode__(self):
        return self.category


class SubCategory(models.Model):
    category = models.ForeignKey(Category, null=True, related_name='subcategories')
    sub_category_name = models.CharField(max_length=20)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'subcategories'

    def __unicode__(self):
        return self.sub_category_name


class Product(models.Model):
    product_name = models.CharField(max_length=30)
    description = models.TextField()
    price = models.PositiveIntegerField()
    image = models.ImageField(upload_to='images', max_length=50)
    category = models.ForeignKey(Category, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = 'Products'

    def __unicode__(self):
        return self.product_name


class CartItem(models.Model):
    cart_id = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True, null=False)
    product = models.ForeignKey(Product, null=False, unique=False)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = 'Cart_Items'
        ordering = ['date_added']

    def total_price(self):
        return self.quantity * self.product.price

    def product_name(self):
        return self.product.product_name

    def price(self):
        return self.product.price

    def augment_quantity(self, quantity):
        self.quantity += int(quantity)
        self.save()

    def product_image(self):
        return self.product.image







