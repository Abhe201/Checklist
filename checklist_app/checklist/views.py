from django.shortcuts import render , redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Service ,Profile,Location
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.utils import timezone
# Create your views here.

def custom_login_view(request):
    if request.method == 'POST':
        # Use Django's AuthenticationForm for validating credentials
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # Get the username and password from the form
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            # Authenticate the user
            user = authenticate(username=username, password=password)
            
            if user is not None:
                # Log the user in
                login(request, user)
                return redirect('checklist')  # Redirect to the checklist page
            else:
                # Invalid credentials
                return render(request, 'registration/login.html', {'form': form, 'error': 'Invalid credentials'})
        else:
            # Invalid form
            return render(request, 'registration/login.html', {'form': form, 'error': 'Invalid form submission'})
    else:
        # Display the login page with an empty form
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