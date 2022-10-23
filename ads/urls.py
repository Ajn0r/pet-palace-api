from django.urls import path
from ads import views

urlpatterns = [
    path('ads/', views.AdList.as_view()),
]
