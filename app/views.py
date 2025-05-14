from itertools import count
from django.shortcuts import redirect, render, get_object_or_404

from app.models import UserModel, UserContact, HospitalModel, DoctorModel, AmbulanceModel
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
import time
from django.db import connection
from .models import HospitalModel


# Create your views here.
def home(request):
    if not request.session.get('email'):
        messages.error(request, 'You need to login first.')
        return redirect('login')
    try:
        user = UserModel.objects.get(email=request.session['email'])
        hospitals = HospitalModel.objects.all()
        doctors = DoctorModel.objects.all()
        ambulances = AmbulanceModel.objects.all()
        contacts = UserContact.objects.all()
        return render(request, 'index.html', {'user': user, 'showSearch': True, 'hospitals': hospitals, 'doctors': doctors, 'ambulances': ambulances, 'contacts': contacts})                                                                            
    except UserModel.DoesNotExist:
        messages.error(request, 'User not found.')
        request.session.flush()
        return redirect('login')
    
def login(request):
    if request.session.get('email'):
        messages.info(request, 'You are already logged in.')
        return redirect('home')                                                                                                                                                                                                                                                                                 

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = UserModel.objects.get(email=email)
            if check_password(password, user.password):
                request.session['email'] = user.email
                messages.success(request, 'Login successful.')
                return redirect('home')
            else:
                messages.error(request, 'Invalid email or password.')
        except UserModel.DoesNotExist:
            messages.error(request, 'Account not found. Please register.')

        return redirect('login')

    return render(request, 'login.html')

def register(request):
    if request.session.get('email'):
        messages.info(request, 'You are already logged in.')
        return redirect('home')

    if request.method == 'POST':
        name = request.POST.get('fullname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        if UserModel.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('register')

        UserModel.objects.create(
            name=name,
            email=email,
            password=make_password(password)
        )

        messages.success(request, 'Registration successful. Please log in.')
        return redirect('login')

    return render(request, 'register.html')


# Logout View
def logout(request):
    if request.session.get('email'):
        request.session.flush()
        messages.success(request, 'Logged out successfully.')
    else:
        messages.info(request, 'You are not logged in.')
    return redirect('login')


def contact(request):
    try:
        user = UserModel.objects.get(email=request.session['email'])

        if request.method == 'POST':
            if request.POST.get('txtname') and request.POST.get('txtEmail') and request.POST.get('txtMsg'):
                saveContact = UserContact()

                saveContact.messengerId = user.id
                saveContact.messengerName = user.name
                saveContact.messengerEmail = user.email
                saveContact.message = request.POST.get('txtMsg')

                saveContact.save()
                time.sleep(3)
                return redirect('/')
        else:
            return render(request, 'contact.html', {'user': user, 'hideBanner': True})
    except:
        messages.error(request, 'You need to login first')
        return redirect('login')

def terms_and_conditions(request):
    return render(request, 'terms_and_conditions.html')

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def admin_panel(request):
    try:
        user = UserModel.objects.get(email=request.session['email'])
        
        hospitals = HospitalModel.objects.all()

        for hsptl in hospitals:
            hsptl.services_list = hsptl.services.split(',') if hsptl.services else []
            hsptl.doctor_count = DoctorModel.objects.filter(hospital_id=hsptl.id).count()
            hsptl.ambulance_count = AmbulanceModel.objects.filter(hospital_id=hsptl.id).count()
            hsptl.departments_list = hsptl.departments.split(',') if hsptl.departments else []

        doctors = DoctorModel.objects.all()

        ambulances = AmbulanceModel.objects.all()

        return render(request, 'admin_panel.html', {'user': user, 'hospitals': hospitals, 'doctors': doctors, 'ambulances': ambulances})
    except:
        messages.error(request, 'You need to login first')
        return redirect('login')

# Add Hospital View
def add_hospital(request):
    if request.method == 'POST':
        if request.POST.get('name') and request.POST.get('location') and request.POST.get('latitude') and request.POST.get('longitude') and request.POST.get('phone') and request.POST.get('email') and request.POST.get('services') and request.POST.get('departments'):
            saveHospital = HospitalModel()

            saveHospital.name = request.POST.get('name')
            saveHospital.location = request.POST.get('location')
            saveHospital.latitude = request.POST.get('latitude')
            saveHospital.longitude = request.POST.get('longitude')
            saveHospital.phone = request.POST.get('phone')
            saveHospital.email = request.POST.get('email')
            saveHospital.services = request.POST.get('services')
            saveHospital.departments = request.POST.get('departments')

            saveHospital.save()
            return redirect('admin_panel')
    else:
        return render(request, 'admin_panel.html')

# Add Doctor View
def add_doctor(request):
    if request.method == 'POST':
        if request.POST.get('name') and request.POST.get('degrees') and request.POST.get('hospital') and request.POST.get('department') and request.POST.get('phone') and request.POST.get('availableDays') and request.POST.get('apointmentTime') and request.POST.get('availableTime') and request.POST.get('fees') and request.POST.get('rating'):
            saveDoctor = DoctorModel()

            hospital = HospitalModel.objects.get(id=request.POST.get('hospital'))
            saveDoctor.name = request.POST.get('name')
            saveDoctor.degrees = request.POST.get('degrees')
            saveDoctor.hospital = hospital
            saveDoctor.department = request.POST.get('department')
            saveDoctor.phone = request.POST.get('phone')
            saveDoctor.availableDays = request.POST.get('availableDays')
            saveDoctor.apointmentTime = request.POST.get('apointmentTime')
            saveDoctor.availableTime = request.POST.get('availableTime')
            saveDoctor.fees = request.POST.get('fees')
            saveDoctor.rating = request.POST.get('rating')
            saveDoctor.link = request.POST.get('link')

            saveDoctor.save()
            return redirect('admin_panel')

    return render(request, 'admin_panel.html')

# # Add Ambulance View
def add_ambulance(request):
    if request.method == 'POST':
        if request.POST.get('name') and request.POST.get('hospital') and request.POST.get('services') and request.POST.get('phone') and request.POST.get('fees'):
            saveAmbulance = AmbulanceModel()

            hospital = HospitalModel.objects.get(id=request.POST.get('hospital'))
            saveAmbulance.name = request.POST.get('name')
            saveAmbulance.hospital = hospital
            saveAmbulance.location = hospital.location
            saveAmbulance.latitude = hospital.latitude
            saveAmbulance.longitude = hospital.longitude
            saveAmbulance.phone = request.POST.get('phone')
            saveAmbulance.services = request.POST.get('services')
            saveAmbulance.fees = request.POST.get('fees')
            saveAmbulance.link = request.POST.get('link')

            saveAmbulance.save()
            return redirect('admin_panel')

    return render(request, 'admin_panel.html')

## doctor page 

def doctors_page(request, hospital_id):
    try:
        user = UserModel.objects.get(email=request.session['email'])
        hospital = HospitalModel.objects.get(id=hospital_id)
        doctors = DoctorModel.objects.filter(hospital_id=hospital_id)

        return render(request, 'doctors_p.html', {
            'user': user,
            'hospital': hospital,
            'doctors': doctors
        })

    except HospitalModel.DoesNotExist:
        messages.error(request, 'Hospital not found.')
        return redirect('admin_panel')  
    except:
        messages.error(request, 'You need to login first')
        return redirect('login')

def delete_hospital(request, hospital_id):
    if request.method == 'POST':
        hospital = get_object_or_404(HospitalModel, id=hospital_id)
        hospital.delete()
        messages.success(request, 'Hospital deleted successfully.')
    return redirect('admin_panel')