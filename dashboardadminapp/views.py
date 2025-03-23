from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse  # ✅ Import reverse
from .models import SuperAdminUser
from .forms import AddUserForm  # ✅ Ensure this exists
import random
from datetime import datetime

def dashboard_view(request):
    return render(request, 'dashboardadminapp/dashboard.html')  # ✅ No need for list_users_url

def add_user(request):
    if request.method == "POST":
        form = AddUserForm(request.POST)
        if form.is_valid():
            lastname = form.cleaned_data['lastname']
            firstname = form.cleaned_data['firstname']
            middle_initial = form.cleaned_data['middle_initial']

            # Generate user_number: year/001/random number
            current_year = datetime.now().year
            random_number = random.randint(100, 999)
            user_number = f"{current_year}001{random_number}"

            # Save user to database
            new_user = SuperAdminUser(
                lastname=lastname,
                firstname=firstname,
                middle_initial=middle_initial,
                user_number=user_number,
                password="Avicast123"  # ✅ Default password
            )
            new_user.save()

            messages.success(request, "User added successfully!")
            return redirect("dashboardadminapp:list_users")  # ✅ Redirect to List of Users

    else:
        form = AddUserForm()

    return render(request, "dashboardadminapp/add_user.html", {"form": form})

def list_users(request):
    users = SuperAdminUser.objects.all()  # ✅ Get all users
    return render(request, 'dashboardadminapp/list_users.html', {'users': users})
