from django.urls import path
from pet_sittings import views

urlpatterns = [
    path('petsittings/', views.PetSittingList.as_view()),
    path('petsittings/<int:pk>', views.PetSittingDetail.as_view()),
]
