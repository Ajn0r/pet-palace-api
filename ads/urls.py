from django.urls import path
from ads import views

urlpatterns = [
    path('ads/', views.AdList.as_view()),
    path('ads/<int:pk>', views.AdDetail.as_view()),
    path('ads/petchoices', views.PetChoices.as_view()),
]
