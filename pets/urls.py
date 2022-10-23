from django.urls import path
from pets import views

urlpatterns = [
    path('pets/', views.PetList.as_view()),
    path('pets/<int:pk>', views.PetDetail.as_view()),
]
