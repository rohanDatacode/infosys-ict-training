from django.shortcuts import render
from .models import Customer

def home(request):
    return render(request, 'home.html')


def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customers/customer_list.html', {'customers': customers})

def add_customer(request):
    # Just placeholder (if you want form later)
    return render(request, 'customers/add_customer.html')
