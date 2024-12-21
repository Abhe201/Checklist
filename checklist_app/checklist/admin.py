from django.contrib import admin
from .models import Service, Profile ,ServiceRecord

# Register Profile model to appear in the admin interface
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location')
    search_fields = ('user__username', 'location')


@admin.register(ServiceRecord)
class ServiceRecordAdmin(admin.ModelAdmin):
    list_display = ('service', 'user', 'date', 'status', 'remarks')
    search_fields = ('service__name', 'user__username', 'status', 'remarks')
    list_filter = ('date', 'status')

# Register the Service model to appear in the admin interface
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    # Display fields in the admin list view
    list_display = ('serial', 'name', 'category', 'ip', 'frequency', 'status', 'remarks', 'display_locations')
    
    # Optional: Allow searching by specific fields
    search_fields = ('name', 'category', 'ip', 'status')
    
    # Filter options in the admin panel
    list_filter = ('status', 'category', 'locations')
    
    # Set default ordering of records
    ordering = ('serial',)
    
    # Allow editing specific fields directly in the list view
    list_editable = ('name', 'category', 'ip', 'status', 'frequency')
    
    # Customize the form in the edit view
    fieldsets = (
        (None, {
            'fields': ('name', 'category', 'ip', 'status', 'frequency', 'remarks', 'locations')
        }),
    )

    # Enable horizontal filter widget for ManyToMany field `locations`
    filter_horizontal = ('locations',)

    # Display locations in the list view as a comma-separated string
    def display_locations(self, obj):
        return ", ".join([location.name for location in obj.locations.all()])
    display_locations.short_description = 'Locations'  # Set column title as 'Locations'
