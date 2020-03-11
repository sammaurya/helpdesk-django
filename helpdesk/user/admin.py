from django.contrib import admin
from django import forms
from  django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model

class AddUserForm(forms.ModelForm):
    """
    New User Form. Requires password confirmation
    """
    password1 = forms.CharField(
        label='Password', widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Confirm Password', widget=forms.PasswordInput
    )
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email', 'department', 'password1', 'password2')

    def cleaned_password(self):
        # Check that the two password entries match
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password1

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_password())
        if commit:
            user.save()
        return user

class UpdateUserForm(forms.ModelForm):
    """
    Update User Form. Doesn't allow changing password in the Admin
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = get_user_model()
        fields = (
            'first_name', 'last_name', 'email', 'password','department','is_active','is_staff'
        )

    def clean_password(self):
       # Password can't be changed in the admin
       return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    form = UpdateUserForm
    add_form = AddUserForm

    list_display = ('first_name','last_name','email','department','is_staff')
    list_filter = ('is_staff','department')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields' : ('is_active', 'is_staff')}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields' : (
                    'first_name', 'last_name', 'email', 'department', 'password1','password2'
                )
            }
        ),
    )

    search_fields = ('email','first_name','last_name','department')
    ordering = ('email','department')
    filter_horizontal = ()

admin.site.register(get_user_model(), UserAdmin)