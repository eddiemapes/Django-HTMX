from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
from django.forms.widgets import SelectDateWidget
from .models import Profile, AccessCredential

# Register your models here.
class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('birthday',)
        widgets = {
            'birthday': SelectDateWidget(years=range(1940, 2011))
        }

class ProfileInline(admin.StackedInline):
    model = Profile
    form = PersonalInfoForm
    can_delete = False
    verbose_name = 'User Profile'
    fieldsets = (
        ('Personal Information', {
            'fields': ('mobile_phone', 'address', 'city', 'state', 'zip_code', 'last_four_ssn', 'birthday', 'personal_email')
        }),
        ('Office Information', {
            'fields': ('office_phone', 'phone_extension', 'ip_address', 'department', 'bonus_rate', 'offer_date', 'start_date', 'term_date')
        }),
    )

class AccessInfoInline(admin.StackedInline):
    model = AccessCredential
    can_delete = False
    verbose_name = 'Access Credentials'
    fields = ('availity_id', 'uhc_id', 'jefferson_campus_key', 'trinity_id')
    max_num = 1

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, AccessInfoInline,)
    
    def get_inline_instances(self, request, obj):
        if not obj:
            return []
        else:
            return super().get_inline_instances(request, obj)
        


admin.site.unregister(User)
admin.site.register(User, UserAdmin)