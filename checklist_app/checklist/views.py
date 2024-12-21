from django.shortcuts import render , redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Service ,Profile,Location , ServiceRecord
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.utils import timezone


from freezegun import freeze_time

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
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Service, Location, ServiceRecord

@freeze_time("2024-01-01")
def checklist_view(request):
    # Get the current user's profile and their default location
    profile = request.user.profile  # Assumes the user has a `profile` with a `location` field
    user_location_name = profile.location  # Get the user's default location (as a string)

    # Fetch the Location instance based on the user's default location
    try:
        location_instance = Location.objects.get(name=user_location_name)
    except Location.DoesNotExist:
        location_instance = None

    # Filter services for the user's location
    if location_instance:
        services = Service.objects.filter(locations=location_instance)
    else:
        services = Service.objects.none()

    # Get the current date in 'day-month-year' format
    # current_date = timezone.now().strftime('%d-%m-%Y')
    current_date = datetime.now().strftime('%d-%m-%Y')

    if request.method == 'POST':
        errors = []
        records_to_save = []  # List to collect `ServiceRecord` objects for bulk creation

        for service in services:
            # Get the status and remarks from the form
            status = request.POST.get(f'status-{service.serial}')
            remarks = request.POST.get(f'remarks-{service.serial}')
            
            # Validation: Remarks are required if status is 'No'
            if status == 'No' and not remarks:
                errors.append(f"Remarks must be provided for service {service.name} (Serial: {service.serial})")
            
            if not errors:
                # Create a `ServiceRecord` instance for this service
                record = ServiceRecord(
                    service=service,
                    date=timezone.now().date(),
                    status=status,
                    remarks=remarks if status == 'No' else ''  # Store remarks only if status is 'No'
                )
                records_to_save.append(record)

                # Update the service's current status and remarks
                service.status = status
                service.remarks = remarks if status == 'No' else ''
                service.updated_at = timezone.now()
                service.save()

        # Save all records in bulk
        if records_to_save:
            ServiceRecord.objects.bulk_create(records_to_save)

        # Handle errors, if any
        if errors:
            return render(request, 'checklist/checklist.html', {
                'services': services,
                'errors': errors,
                'current_date': current_date,
                'location': profile.location,
            })

        # Redirect back to the checklist page after successful submission
        return redirect('checklist')

    # Render the checklist page with services and context
    return render(request, 'checklist/checklist.html', {
        'services': services,
        'current_date': current_date,
        'location': profile.location,
    })

def record_view(request):
    records = ServiceRecord.objects.all().order_by('-date')  # Fetch all records sorted by date
    return render(request, 'record/record.html', {'records': records})

