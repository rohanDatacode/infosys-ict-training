from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='customer_home'),  # ✅ add this line
    path('add/', views.add_customer, name='add_customer'),
    path('list/', views.customer_list, name='customer_list'),
]
