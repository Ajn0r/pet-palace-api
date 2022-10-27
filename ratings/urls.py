from django.urls import path
from ratings import views

urlpatterns = [
    path('ratings/', views.RatingList.as_view()),

]