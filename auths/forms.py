from django import forms
from .models import *

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ["full_name", "phone_number", "role"]

class UserForm(forms.ModelForm):
    full_name=forms.CharField(label='Full name',required=True)
    phone_number = forms.CharField(label='First Mobile number', required=True)
    role=forms.ModelChoiceField(queryset=Role.objects.filter(is_active=True))

    class Meta:
        model = User
        fields = ["is_active", "is_staff", 'email','username','full_name','role','phone_number',]


class RoleForm(forms.ModelForm):
    perm=forms.ModelMultipleChoiceField(
        queryset=CustPermission.objects.filter(is_single=False),
        widget=forms.CheckboxSelectMultiple, required=True, label='PERMISSION LIST')
    perm_one_only = forms.ModelChoiceField(
        queryset=CustPermission.objects.filter(is_single=True),
        widget=forms.RadioSelect, required=False, label='Special Permission')
    class Meta:
        model = Role
        fields = ["role_name","perm"]

    def clean_role_name(self):
        role_name = self.cleaned_data["role_name"]
        if  Role.objects.filter(role_name__iexact=str(role_name)).exists():
            raise forms.ValidationError('Such role exists either in active or inactive')
        return role_name

class RoleEditForm(forms.ModelForm):
    perm=forms.ModelMultipleChoiceField(
        queryset=CustPermission.objects.filter(is_single=False),
        widget=forms.CheckboxSelectMultiple, required=True, label='PERMISSION LIST')
    perm_one_only = forms.ModelChoiceField(
        queryset=CustPermission.objects.filter(is_single=True),
        widget=forms.RadioSelect, required=False, label='Special Permission')
    class Meta:
        model = Role
        fields = ["role_name","perm"]


class PermissionForm(forms.ModelForm):
    class Meta:
        model = CustPermission
        fields = ["perm_name",'perm_desc']
        

class PasswordForm(forms.ModelForm):
    class Meta:
        model = DefaultPassword
        fields = ["password"]

class UserUpdateFormPass(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(),label='Old Password')
    new_password = forms.CharField(widget=forms.PasswordInput(),label='New Password')
    cpassword = forms.CharField(widget=forms.PasswordInput(), label='Confirm Password')
    class Meta:
        model = DefaultPassword
        fields = ["password"]

class CustomAuthenticationForm(forms.Form):
    username=forms.CharField(label='MemberNo',required=True)

class CustomAuthCodeForm(forms.Form):
    auth_code=forms.CharField(label='Auth code',required=True)
