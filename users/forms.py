from urllib import request

from django import forms
from django.contrib.auth.models import User

from actions.models import Action


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    email_subscribe = forms.ChoiceField(
        choices=[('yes', 'Yes'), ('no', 'No')],
        widget=forms.Select,
        label='Email Subscription'
    )
    role = forms.ChoiceField(
        choices=[('admin', 'Admin'), ('regular', 'Regular')],
        widget=forms.Select(attrs={'class': 'input-box'}),
    )

    def __init__(self, *args, **kwargs):
        user_role = kwargs.pop('user_role', None)
        super(UserProfileForm, self).__init__(*args, **kwargs)

        if user_role != 'admin':
            del self.fields['role']

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'email_subscribe', 'role']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'input-box'}),
            'last_name': forms.TextInput(attrs={'class': 'input-box'}),
            'email': forms.EmailInput(attrs={'class': 'input-box'}),
            'password': forms.PasswordInput(attrs={'class': 'input-box'}),
            'email_subscribe': forms.Select(attrs={'class': 'input-box'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        return password

    def save(self, commit=True):
        user = super(UserProfileForm, self).save(commit=False)

        new_password = self.cleaned_data.get("password")
        if new_password:
            user.set_password(new_password)
        else:
            print("save - No new password submitted")

        role_changed = False
        new_role = self.cleaned_data.get('role')

        # If new_role is None, stay the same
        if new_role is None:
            new_role = user.details.role

        # check if role is changing
        if user.details.role != new_role:
            role_changed = True
            user.details.role = new_role

        email_subscribe = self.cleaned_data.get('email_subscribe')
        user.details.email_subscribe = email_subscribe == 'yes'

        if commit:
            print("save - User before save:", user.password)
            print("User authenticated before save:", user.details.role)
            # print("User authenticated before save:", request.user.is_authenticated)
            user.save()
            print("save - User after save:", user.password)
            print("User authenticated after save:", user.details.role)
            # print("User authenticated after save:", request.user.is_authenticated)
            user.details.save()
            print("User and details saved")

        if role_changed:
            action = Action(user=user, verb="'s role has been changed")
            action.save()

        return user
