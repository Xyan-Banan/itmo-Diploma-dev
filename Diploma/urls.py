from django.urls import path
from . import views

app_name = 'Diploma'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('profile/create_practice', views.create_practice, name='create_practice'),

]
