import uuid
from datetime import timedelta

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.utils.timezone import now
from users.models import User, EmailVerification


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=True)
        expiration_date = now() + timedelta(hours=48)
        record = EmailVerification.objects.create(code=uuid.uuid4(), user=user, expiration_date=expiration_date)
        record.send_verification()
        return user


class UserProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'country', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()


class PasswordRecoveryForm(forms.Form):
    email = forms.EmailField(label='Email')
