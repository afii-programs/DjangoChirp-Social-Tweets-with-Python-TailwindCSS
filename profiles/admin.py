from django.contrib import admin
from .models import Profiles, Skill

# Register your models here.

class ProfilesAdmin(admin.ModelAdmin):
    pass

class SkillAdmin(admin.ModelAdmin):
    pass

admin.site.register(Profiles, ProfilesAdmin)
admin.site.register(Skill, ProfilesAdmin)