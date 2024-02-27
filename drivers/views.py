from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from drivers.models import Driver, CarDriver

from .forms import RegistrationForm, DriverForm
from AutoparkProject.utils import calculate_age
from AutoparkProject.settings import LOGIN_REDIRECT_URL
from employees.models import Car


def index(request):
    title = "Главная страница"
    context = {"title": title}
    return render(request, "drivers/index.html", context=context)

def register(request):
    if request.method == "POST":
        reg_form = RegistrationForm(request.POST)
        driver_form = DriverForm(request.POST)

        if reg_form.is_valid() and driver_form.is_valid():
            user = reg_form.save()
            driver = driver_form.save(commit=False)
            driver.user = user
            driver.age = calculate_age(driver.birthday)
            driver.save()
            #return redirect("driver_profile")
            return register_done(request, new_user=driver)
        
    reg_form = RegistrationForm()
    driver_form = DriverForm()
    context = {"reg_form": reg_form, "driver_form": driver_form}

    return render(request, "drivers/register.html", context=context)
        
def register_done(request, new_user):
    context = {"driver": new_user, "title": "Успешная регистрация"}
    return render(request, "drivers/register_done.html", context=context)

def log_in(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                url = request.GET.get('next', LOGIN_REDIRECT_URL)
                return redirect(url)
    return render (request, 'drivers/login.html', {'form': form, 'title': "Вход"})     


def log_out(request):
    logout(request)
    url = LOGIN_REDIRECT_URL
    return redirect(url)      


def select_car(request, pk=None):
    if request.method == "GET":
        title = "Выберите машину"
        cars = Car.objects.filter(status=True)
        car_count = Car.objects.filter(status=True).count()
        context = {"title": title, "cars": cars, "count": car_count}
    if pk is not None:
        print (pk)
        car = Car.objects.get(pk=pk)
        car.status = False
        car.save()

        driver = Driver.objects.get(pk=request.user.pk)
        driver_on_car = CarDriver.objects.create(car=car)

        return redirect("drivers:index")

    return render(request, "drivers/select_car.html", context=context)

@csrf_exempt
def test_fetch(request):
    if request.method == "POST":
        json_data = json.loads(request.body)
        car_id = json_data.get('id')

    return JsonResponse({'car_id': car_id})

def profile(request, pk):
    driver = Driver.objects.get(pk=pk)
    car_driver = CarDriver.objects.filter(driver=driver).first()
    if car_driver is not None:
        car = car_driver.car
    else:
        car = None
    
    context = {'driver': driver, 'car': car}
    return redirect(request, 'drivers/profile.html', context=context)
