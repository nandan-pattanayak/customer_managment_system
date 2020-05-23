from django.shortcuts import render,redirect
from .models import *
from .forms import OrderForm,CreateUserForm,AccountForm
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticate_user,allow_user,admin_only
# Create your views here.
@login_required(login_url='login')
@admin_only
def home(request):
	customer=Customer.objects.all()
	order=Order.objects.all()
	total_order=order.count()
	delivered=Order.objects.filter(status='Delivered').count()
	pending=Order.objects.filter(status='Pending').count()
	context={
	'customers':customer,
	'products':order,
	'order_delivered':delivered,
	'order_pending':pending,
	'total_order':total_order
	}
	return render(request,'home.html',context)
@login_required(login_url='login')
@allow_user(allow=['admin'])
def customer(request,pk):
	customer=Customer.objects.get(id=pk)
	order=customer.order_set.all()
	myfilter=OrderFilter(request.POST,queryset=order)
	order=myfilter.qs
	context={
	'customer':customer,
	'orders':order,
	'myfilter':myfilter
	}
	return render(request,'customer.html',context)
@login_required(login_url='login')
@allow_user(allow=['admin'])
def product(request):
	product=Product.objects.all()
	context={
	'products':product
	}
	return render(request,'product.html',context)
@login_required(login_url='login')
@allow_user(allow=['admin'])
def updateorder(request,pk):
	order=Order.objects.get(id=pk)
	form=OrderForm(instance=order)
	if request.method == 'POST':
		form=OrderForm(request.POST,instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')
	context={
	'formset':form
	}
	return render(request,'order_form.html',context)

@login_required(login_url='login')
@allow_user(allow=['admin'])
def deleteorder(request,pk):
	order=Order.objects.get(id=pk)
	if request.method == 'POST':
		order.delete()
		return redirect("/")
	context={
	'item':order.product.name
	}
	return render(request,'delete_order.html',context)
@login_required(login_url='login')
@allow_user(allow=['admin'])
def createorder(request,pk):
	customer=Customer.objects.get(id=pk)
	createorderform=inlineformset_factory(Customer,Order,fields=['product','status'],extra=10)
	formset=createorderform(instance=customer)
	if request.method == 'POST':
		formset=createorderform(request.POST,instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect("/")
	context={
	'formset':formset
	}
	return render(request,'order_form.html',context)
@unauthenticate_user
def register(request):
	form=CreateUserForm()
	if request.method == 'POST':
		form=CreateUserForm(request.POST)
		if form.is_valid():
			user=form.save()
			group=Group.objects.get(name='customer')
			user.groups.add(group)
			Customer.objects.create(user=user)
			username=form.cleaned_data.get('username')
			messages.info(request,f'Account Created for {username}!!')
			return redirect("login")
	context={
	'form':form
	}
	return render(request,'register.html',context)
@unauthenticate_user
def login(request):
	if request.method == 'POST':
		username=request.POST.get('username')
		password=request.POST.get('password')
		user=authenticate(request,username=username,password=password)
		if user is not None:
			auth_login(request,user)
			return redirect("/")
		else:
			messages.info(request,f"Please Enter Valid username and password")
	return render(request,'login.html')

def logout(request):
	auth_logout(request)
	return redirect('login')
@allow_user(allow=['customer'])
def user(request):
	order=request.user.customer.order_set.all()
	total_order=order.count()
	delivered=order.filter(status='Delivered').count()
	pending=order.filter(status='Pending').count()
	context={
	'total_order':total_order,
	'order_delivered':delivered,
	'order_pending':pending,
	'orders':order
	}
	return render(request,'user.html',context)
@allow_user(allow=['customer'])
def account_setting(request):
	customer=request.user.customer
	form=AccountForm(instance=customer)
	if request.method == 'POST':
		form=AccountForm(request.POST,request.FILES,instance=customer)
		form.save()
	context={
	'form':form
	}
	return render(request,'account_setting.html',context)