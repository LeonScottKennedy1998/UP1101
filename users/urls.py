from . import views
from django.urls import path,include


urlpatterns = [
    path('', views.home, name= "home"),
    path("signup/", views.SignUp.as_view(),name="signup")

]