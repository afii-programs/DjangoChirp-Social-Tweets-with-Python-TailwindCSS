from django.contrib import admin
from .models import Profiles

# Register your models here.

class ProfilesAdmin(admin.ModelAdmin):
    pass

admin.site.register(Profiles, ProfilesAdmin)