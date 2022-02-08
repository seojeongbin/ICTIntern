# users/urls.py

from django.urls import path
from . import views


urlpatterns = [
    path('agreement/', views.AgreementView.as_view(), name='agreement'),
]