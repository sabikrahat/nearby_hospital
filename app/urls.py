from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('privacy-policy', views.privacy_policy, name="privacy-policy"),
    path('terms-and-conditions', views.terms_and_conditions, name="terms-and-conditions"),
    path('contact', views.contact, name="contact"),
    path('admin_panel', views.admin_panel, name="admin_panel"),
    path('add_hospital', views.add_hospital, name='add_hospital'),
    path('add_doctor', views.add_doctor, name='add_doctor'),
    path('add_ambulance', views.add_ambulance, name='add_ambulance'),
    path('doctors/<int:hospital_id>/', views.doctors_page, name='doctors_page'),
    path('hospital/delete/<int:hospital_id>/', views.delete_hospital, name='delete_hospital'),

]
