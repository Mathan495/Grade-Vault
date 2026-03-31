from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_page, name="login_page"),
    path('logout/', views.logout_page, name="logout"),
    path('register/', views.register_page, name="register_page"),
    path('profile/', views.profile_page, name="profile"),
    path('add_semester/', views.add_semester_page, name="add_semester"),
    path('get_subjects/', views.get_subjects, name='get_subjects'), 
]
