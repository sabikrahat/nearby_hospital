from django.shortcuts import redirect, render

from app.models import UserModel, UserContact
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
import time

# Create your views here.
def home(request):
    if not request.session.get('email'):
        messages.error(request, 'You need to login first.')
        return redirect('login')
    try:
        user = UserModel.objects.get(email=request.session['email'])
        return render(request, 'index.html', {'user': user})
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
            return render(request, 'contact.html', {'user': user})
    except:
        messages.error(request, 'You need to login first')
        return redirect('login')

def terms_and_conditions(request):
    return render(request, 'terms_and_conditions.html')

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def admin_panel(request):
    return render(request, 'admin_panel.html')



