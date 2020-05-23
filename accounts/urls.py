from django.urls import path
from .import views
urlpatterns=[

   path('',views.home,name='home'),
   path('customer/<str:pk>/',views.customer,name='customer'),
   path('product/',views.product,name='product'),
   path('updateorder/<str:pk>/',views.updateorder,name='updateorder'),
   path('deleteorder/<str:pk>/',views.deleteorder,name='deleteorder'),
   path('createorder/<str:pk>/',views.createorder,name='createorder'),
   path('register/',views.register,name='register'),
   path('login/',views.login,name='login'),
   path('logout/',views.logout,name='logout'),
   path('user/',views.user,name='user'),
   path('account_setting/',views.account_setting,name='account_setting')
 
 
]