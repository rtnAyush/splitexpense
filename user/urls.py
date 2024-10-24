from django.urls import path
from . import views

urlpatterns = [
    path('create/',views.createUser ),
    path('get/<int:userId>',views.getUserById ),
]