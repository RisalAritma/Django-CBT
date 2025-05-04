from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Selamat datang, anda berhasil login!')
            next_url = request.GET.get('next', 'exam:exam_home')  # Redirect ke 'next' jika ada, atau ke halaman utama
            return redirect(next_url)
    else:
        form = AuthenticationForm()
        messages.info(request, 'Silahkan login menggunakan akun anda')  

    return render(request, 'login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Akun anda berhasil dibuat! Silahkan login.')
            return redirect('login')
        else:
            messages.error(request, 'Periksa kembali form anda, ada yang salah!')
    else:
        form = UserCreationForm()
        messages.info(request, 'Lengkapi form di bawah ini untuk mendaftar!')  
    
    return render(request, 'signup.html', {'form': form})
