from django.urls import path
from . import views

app_name = 'Diploma'

urlpatterns = [
    path('login/',views.login,name='login'),
    path('profile/',views.profile,name='profile'),
    path('profile/create_practice',views.themes,name='create_practice'),
]