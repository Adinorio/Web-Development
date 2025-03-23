from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.urls import reverse  # ✅ Import `reverse` for named URLs
from .forms import LoginForm

def user_login(request):
    next_url = request.GET.get('next')  # ✅ Only get `next` if provided

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            ID_number = form.cleaned_data['ID_number']
            password = form.cleaned_data['password']
            user = authenticate(request, ID_number=ID_number, password=password)

            if user is not None:
                login(request, user)
                
                # ✅ If `next_url` exists, go there, otherwise, go to the dashboard
                return redirect(next_url if next_url else reverse('dashboardadminapp:dashboard'))  
            else:
                messages.error(request, "Invalid ID Number or Password.")

    else:
        form = LoginForm()

    return render(request, 'superadminloginapp/login.html', {'form': form})


