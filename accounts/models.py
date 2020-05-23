from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
	user=models.OneToOneField(User,null=True,on_delete=models.CASCADE)
	name=models.CharField(max_length=30,null=True)
	email=models.CharField(max_length=30,null=True)
	phone=models.CharField(max_length=30,null=True)
	date=models.DateTimeField(auto_now_add=True,null=True)
	image=models.ImageField(default='cart2.jpeg',null=True)
	def __str__(self):
		return self.name

class Product_Type(models.Model):
	name=models.CharField(max_length=30,null=True)
	def __str__(self):
		return self.name

class Product(models.Model):
	CATEGORY=(('Indoor','Indoor'),('Out Door','Out Door'))
	name=models.CharField(max_length=30,null=True)
	price=models.FloatField(null=True)
	category=models.CharField(max_length=30,null=True,choices=CATEGORY)
	description=models.CharField(max_length=30,null=True,blank=True)
	tags=models.ManyToManyField(Product_Type)
	date=models.DateTimeField(auto_now_add=True,null=True)


	def __str__(self):
		return self.name

class Order(models.Model):
		STATUS=(('Delivered','Delivered'),('Pending','Pending'),('Out Of Delivery','Out of Delivery'))
		customer=models.ForeignKey(Customer,null=True,on_delete=models.SET_NULL)
		product=models.ForeignKey(Product,null=True,on_delete=models.SET_NULL)
		status=models.CharField(max_length=30,null=True,choices=STATUS)
		date=models.DateTimeField(auto_now_add=True,null=True)
		def __str__(self):
			return self.product.name