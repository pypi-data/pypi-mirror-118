from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import  views

urlpatterns = [
    path(r'medical/assets/', csrf_exempt(views.get_data))
]