from django.urls import path
from app_messages import views

urlpatterns = [
    path('messages/', views.AppMessageList.as_view()),
    path('messages/new', views.AppMessageCreate.as_view()),
]
