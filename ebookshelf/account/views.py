from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User, auth
from django.contrib import messages

# Create your views here.
@csrf_protect
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('login')
    return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')

@csrf_protect
def signup(request):
    try:
        if request.method == 'POST':
            if 'first_name' in request.POST:
                first_name = request.POST['first_name']
            else:
                first_name = ''
            if 'last_name' in request.POST:
                last_name = request.POST['last_name']
            else:
                last_name = ''

            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            if 'username' in request.POST:
                username = request.POST['username']
            else:
                messages.info(request, 'Username is required')
                return redirect('signup')
            if password1==password2:
                if User.objects.filter(username=username).exists():
                    messages.info(request, 'Username already eixst')
                    return redirect('signup')
                elif User.objects.filter(email=email).exists():
                    messages.info(request, 'Email already eixst')
                    return redirect('signup')
                else:
                    user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username,email=email,password=password1)
                    user.save();
                    return redirect('login')

            else:
                messages.info(request, 'Password do not match')
                return redirect('signup')
    except Exception as e:
        messages.info(request, e)
        return redirect('signup')

        
    
    return render(request, 'signup.html')


def user_page(request):
    return render(request, 'userpage.html')