# forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from exam.models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20)
    address = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'phone', 'address']

    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data['email']
        user.email = email
        user.username = email  # Set username sama dengan email
        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                phone=self.cleaned_data['phone'],
                address=self.cleaned_data['address']
            )
        return user
