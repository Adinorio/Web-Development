from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from .models import SuperAdminUser
from .forms import AddUserForm
import random
from datetime import datetime

def dashboard_view(request):
    list_users_url = reverse('dashboardadminapp:list_users')  # ✅ Correct namespace
    return render(request, 'dashboardadminapp/dashboard.html', {'list_users_url': list_users_url})

def add_user(request):
    if request.method == "POST":
        form = AddUserForm(request.POST)
        if form.is_valid():
            lastname = form.cleaned_data['last_name']
            firstname = form.cleaned_data['first_name']
            middle_initial = form.cleaned_data['middle_initial']

            # Generate user_number: year/001/random number
            current_year = datetime.now().year
            random_number = random.randint(100, 999)
            user_number = f"{current_year}001{random_number}"

            # Save user to database
            new_user = SuperAdminUser(
                last_name=lastname,
                first_name=firstname,
                middle_initial=middle_initial,
                user_number=user_number,
                password="Avicast123"  # ✅ Default password
            )
            new_user.save()

            messages.success(request, "User added successfully!")
            return redirect("dashboardadminapp:list_users")

    else:
        form = AddUserForm()

    return render(request, "dashboardadminapp/add_user.html", {"form": form})

def list_users(request):
    users = SuperAdminUser.objects.filter(is_archived=False)  # ✅ Show only non-archived users
    return render(request, 'dashboardadminapp/list_users.html', {'users': users})


def edit_user(request, user_id):
    user = get_object_or_404(SuperAdminUser, id=user_id)
    if request.method == "POST":
        form = AddUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "User updated successfully!")
            return redirect("dashboardadminapp:list_users")
    else:
        form = AddUserForm(instance=user)

    return render(request, "dashboardadminapp/edit_user.html", {"form": form, "user": user})

def archive_user(request, user_id):
    user = get_object_or_404(SuperAdminUser, id=user_id)
    user.is_archived = True  # ✅ Mark as archived
    user.save()
    messages.success(request, "User archived successfully!")
    
    # ✅ Redirect to the list of users so the archived user disappears immediately
    return redirect("dashboardadminapp:list_users")

def archived_users(request):
    users = SuperAdminUser.objects.filter(is_archived=True)
    return render(request, 'dashboardadminapp/archived_users.html', {'users': users})  # ✅ Ensure this path is correct


def restore_user(request, user_id):
    user = get_object_or_404(SuperAdminUser, id=user_id)
    user.is_archived = False  # ✅ Restore user
    user.save()
    messages.success(request, "User restored successfully!")
    return redirect("dashboardadminapp:archived_users")