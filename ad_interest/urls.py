from django.urls import path
from ad_interest import views

urlpatterns = [
    path('interest/', views.InterestList.as_view()),
    path('interest/<int:pk>', views.InterestDetail.as_view()),
]
