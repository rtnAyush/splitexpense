from django.urls import path
from . import views

urlpatterns = [
    path('create/',views.createUser ),
    path('get/<int:user_id>',views.getUserById ),
]