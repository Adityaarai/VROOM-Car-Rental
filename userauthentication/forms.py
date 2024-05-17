from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    username = forms.CharField(max_length=150, required=True)

    class Meta:
        model = Profile
        fields = ['address', 'license_number', 'contact']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].initial = self.user.first_name
        self.fields['last_name'].initial = self.user.last_name
        self.fields['email'].initial = self.user.email
        self.fields['username'].initial = self.user.username

    def save(self, commit=True):
        profile = super(UserProfileForm, self).save(commit=False)
        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']
        if commit:
            user.save()
            profile.save()
        return profile
