from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from exam.models import Profile





def login_view(request):
    if request.method == "POST":
        print (request.POST)
        username_in = request.POST['email']
        password_in = request.POST['password']
        user = authenticate(request, username=username_in, password=password_in)        
        if user is not None:
            login(request, user)
            print(user)
            messages.success(request, 'Selamat Datang!')
            return redirect('/exam/')
        else:
            messages.warning(request, 'Periksa Kembali Username dan Password Anda!')
    
    context ={
        'title': 'Login',
        'heading': 'Login Pengguna', 
    }

    if request.user.is_authenticated:
        return redirect('/exam/')
    else:
        return render(request, 'login.html', context)


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Anda telah berhasil keluar.')
    return redirect('login') 

    

def signup_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        # Validasi dasar
        if password1 != password2:
            messages.error(request, "Password tidak cocok.")
            return redirect('signup')

        if User.objects.filter(username=email).exists():
            messages.error(request, "Usurname sudah digunakan.")
            return redirect('signup')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email sudah digunakan.")
            return redirect('signup')

        # Simpan user
        user = User.objects.create(
            username=email,
            email=email,
            password=make_password(password1)
        )
        # Simpan profil terkait
        Profile.objects.create(
            user=user,
            phone=phone,
            address=address
        )

        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect('login')
    
    context ={
        'title': 'Sign Up',
        'heading': 'Daftar Pengguna', 
    }

    return render(request, 'signup.html', context)    
