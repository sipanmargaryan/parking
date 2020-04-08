from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

import users.models


class UserCreationForm(forms.ModelForm):

    class Meta:
        fields = ('phone_number', 'password', 'email', 'first_name', 'avatar', 'date_joined', 'last_login',
                  'last_name', 'country', 'is_staff', 'is_superuser', 'is_active'),

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    ordering = ('phone_number', )
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password', 'email', 'first_name', 'avatar', 'date_joined', 'last_login',
                       'last_name', 'country', 'is_staff', 'is_superuser', 'is_active'),
        }),
    )
    list_display = ('phone_number', 'email', 'first_name', 'last_name', 'is_staff')


admin.site.register(users.models.User, CustomUserAdmin)
admin.site.register(users.models.Car)
admin.site.register(users.models.Notification)
