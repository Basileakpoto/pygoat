from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib import messages
from .models import UserData
from .forms import UserLoginForm, UserRegisterForm, UserDataForm
import random
import string

def index(request):
    # main landing pg
    return render(request, 'index.html')

def about(request):
    # about pg nothing special
    return render(request, 'about.html')

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}! You are now logged in.')
                return redirect('profile')
            else:
                messages.error(request, 'Invalid username or password. Please try again.')
    else:
        form = UserLoginForm()
    
    return render(request, 'login.html', {'form': form})

def generate_api_key():
    # generate a random api key
    # I should probably use a better method but this works for now
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choices(chars, k=16))  # 16 chars should be enough right?

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = User.objects.create_user(username=username, password=password)
            
            # Creating sensitive data for the user
            # Yeah i know this is dummy data but works for demo
            UserData.objects.create(
                user=user,
                credit_card='4111111111111111',  # test visa card number lol
                ssn='123456789',  # not a real SSN obvs
                api_key=generate_api_key()  # not very secure api key but whatever
            )
            
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    
    return render(request, 'register.html', {'form': form})

@login_required
def profile_view(request):
    user_data, created = UserData.objects.get_or_create(
        user=request.user,
        defaults={
            'credit_card': '4111111111111111',
            'ssn': '123456789',
            'api_key': generate_api_key(),
        }
    )

    if request.method == 'POST':
        form = UserDataForm(request.POST)

        if form.is_valid():
            user_data.credit_card = form.cleaned_data['credit_card']
            user_data.ssn = form.cleaned_data['ssn']
            user_data.save(update_fields=['credit_card', 'ssn'])

            messages.success(request, 'Données fictives enregistrées.')
            return redirect('profile')
    else:
        form = UserDataForm(initial={
            'credit_card': user_data.credit_card,
            'ssn': user_data.ssn,
        })

    return render(request, 'profile.html', {
        'user_data': user_data,
        'form': form,
    })

@login_required
def api_data_view(request):
    # FIXME: this is insecure AF - just for demo purposes!!
    # sends all user data as json - bad practice!!
    try:
        user_data = UserData.objects.get(user=request.user)
    except UserData.DoesNotExist:
        # If no user data exists, create some dummy data for demo
        user_data = UserData.objects.create(
            user=request.user,
            credit_card='4111111111111111',  # test card number
            ssn='123456789',  # demo SSN
            api_key=generate_api_key()  # simple api key
        )
    
    data = {
        'username': request.user.username,
        'credit_card': user_data.credit_card,
        'ssn': user_data.ssn,
        'api_key': user_data.api_key
    }
    # Intentionally exposing sensitive data through API
    # cuz we're teaching about data exposure, duh!
    return JsonResponse(data)

def all_users_data_view(request):
    # Vérifier les droits AVANT de consulter les données
    if not request.user.is_authenticated:
        return JsonResponse(
            {'error': 'Authentication required'},
            status=401
        )

    if not request.user.is_staff:
        return JsonResponse(
            {'error': 'Staff access required'},
            status=403
        )

    # Le staff ne reçoit que les informations nécessaires
    all_users_data = []

    for user_data in UserData.objects.select_related('user').all():
        all_users_data.append({
            'username': user_data.user.username,
            'credit_card': '************' + user_data.credit_card[-4:],
            'ssn': '*****' + user_data.ssn[-4:],
        })

    return JsonResponse({'users': all_users_data})

def logout_view(request):
    # simple logout nothing fancy
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('index')

def sensitive_data_exposure_lesson(request):
    # lessons page
    return render(request, 'lesson.html')

@login_required
def staff_dashboard(request):
    if not request.user.is_staff:
        return render(request, 'staff_access_denied.html', status=403)

    utilisateurs = UserData.objects.select_related('user').all()

    return render(request, 'staff_dashboard.html', {
        'utilisateurs': utilisateurs,
})