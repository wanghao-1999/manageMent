from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model
from .models import Department

CustomUser = get_user_model()


class EditUserForm(UserChangeForm):
    new_password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'full_name', 'department', 'new_password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:
            self.fields['username'].widget.attrs['readonly'] = True

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data.get('new_password')
        if new_password:
            user.set_password(new_password)
        if commit:
            user.save()
        return user


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']


class UserForm(forms.ModelForm):
    department = forms.ModelChoiceField(queryset=Department.objects.all(), empty_label="选择部门", required=False)
    email = forms.EmailField(required=False)
    full_name = forms.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'full_name', 'department', 'password']
