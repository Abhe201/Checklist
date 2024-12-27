from django.shortcuts import render , redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Service ,Profile,Location ,DailyRecord
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Q
# Create your views here.

def custom_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Authenticate user (case insensitive for username)
            user = authenticate(username=username.lower(), password=password)
            if user:
                login(request, user)

                # Redirect based on user type
                if hasattr(user, 'profile') and user.profile.user_type == 'Admin':
                    return redirect('records')  # Admin -> Report page
                return redirect('checklist')  # Regular user -> Checklist page

            return render(request, 'registration/login.html', {'form': form, 'error': 'Invalid credentials'})

        return render(request, 'registration/login.html', {'form': form, 'error': 'Invalid form data'})

    form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


# @login_required
def checklist_view(request):
    # Get the current user's profile
    profile = request.user.profile  # Access the user's profile
    user_location_name = profile.location  # Get the user's default location (assumed to be a string)

    # Fetch the Location instance that matches the user's location (e.g., 'Noida')
    try:
        location_instance = Location.objects.get(name=user_location_name)
    except Location.DoesNotExist:
        # Handle the case where the location does not exist (e.g., 'Noida' not in Location table)
        location_instance = None

    if location_instance:
        # Filter services associated with the user's location (ManyToManyField)
        services = Service.objects.filter(locations=location_instance)
    else:
        # If location does not exist, return an empty queryset or handle it as needed
        services = Service.objects.none()

    current_date = timezone.now().strftime('%d-%m-%Y')  # Format the current date as 'day-month-year'

    if request.method == 'POST':
        errors = []
        for service in services:
            status = request.POST.get(f'status-{service.serial}')
            remarks = request.POST.get(f'remarks-{service.serial}')
            
            # Error handling if 'No' is selected but no remarks are provided
            if status == 'No' and not remarks:
                errors.append(f"Remarks must be provided for service {service.name} (Serial: {service.serial})")
            
            # Update status and remarks if no errors
            if not errors:
                service.status = status
                service.remarks = remarks if status == 'No' else ''  # Remarks should only be set if status is 'No'
                service.updated_at = timezone.now()  # Set the updated date to the current time
                service.save()

        # If there are errors, render the checklist with error messages
        if errors:
            return render(request, 'checklist/checklist.html', {
                'services': services,
                'errors': errors,
                'current_date': current_date,
                'location': profile.location,
            })
        
        # Redirect to the checklist page after successful submission
        return redirect('checklist')
    
    # Render the template with the services and additional context
    return render(request, 'checklist/checklist.html', {
        'services': services,
        'current_date': current_date,
        'location': profile.location,
    })

# @login_required
def record_view(request):
    # Check if the user is an Admin
    if request.user.profile.user_type != "Admin":
        return render(request, "checklist/error.html", {"error": "You do not have permission to view this page."})
    
    # Fetch date filter from the request (if provided)
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Fetch location filter from the request (if provided)
    location_filter = request.GET.get('location')

    # Get the DailyRecord queryset based on filters
    records = DailyRecord.objects.all()

    if start_date and end_date:
        records = records.filter(date__range=[start_date, end_date])

    if location_filter:
        records = records.filter(location__name=location_filter)

    # Pass the records to the template
    return render(request, "checklist/report.html", {
        "records": records,
        "start_date": start_date,
        "end_date": end_date,
        "location_filter": location_filter,
    })