from django.urls import path

from core.views import *

urlpatterns = [
    path('', home, name='home'),
    path('login/', loginuser, name='login'),
    path('register/', registeruser, name='register'),
    path('api/login/', LoginUserAPI.as_view(), name='login'),
    path('api/register/', RegisterUserAPI.as_view(), name='register'),
    path('api/task/', TaskList.as_view(), name='task'),
    path('api/task/<int:id>', TaskDetails.as_view(), name='task-details')
]