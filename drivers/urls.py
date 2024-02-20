from django.urls import path
from .views import register, register_done, index, log_in, log_out, select_car


app_name = "drivers"
urlpatterns = [
    path('', index, name='index'),

    path('register/', register, name="register"),
    path('register_done/', register_done, name="register_done"),
    path('login/', log_in, name="login"),
    path('logout/', log_out, name="logout"),

    #path('profile/', profile, name="profile"),

    path('select_car/', select_car, name="select_car")
    
]