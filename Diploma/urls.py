# from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'Diploma'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('profile/create_practice', views.create_practice, name='create_practice'),
    path('profile/show_practice/<practice_id>', views.show_practice, name='show_practice'),
    # url(r'profile/show_practice/(?P<practice_id>.+)$', views.show_practice, name='show_practice'),
]
