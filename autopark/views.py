from datetime import date
from django.shortcuts import render, redirect
from django.views.generic import CreateView

from .models import Driver
from .forms import DriverForm, RegistrationForm

def calculate_age(birthday):
    today = date.today()
    age = today.yaer - birthday.yaer
    if today.month < birthday.month or (today.month == birthday.month and today.day < birthday.day):
        age -= 1
    return age    


# =======DRIVER=========

def driver_registration(request):
    if request.method == "POST":
        reg_from = RegistrationForm(request.POST)
        driver_form = DriverForm(request.POST)

        if reg_from.is_valid() and driver_form.is_valid():
            user = reg_from.save()
            driver = driver_form.save(commit=False)
            driver.user = user
            driver.age = calculate_age(driver.birthday)
            driver.save()
            #return redirect("driver_profile")
            return render(request, "autopark/driver_profile.html", {"driver": driver})
        
    reg_from = RegistrationForm()
    driver_form = DriverForm()
    context = {"reg_form": reg_from, "driver_form": driver_form}

    return render(request, "autopark/driver_form.html", context=context)
        

def driver_profile(reqest, pk):
    driver = Driver.objects.get(pk=pk)
