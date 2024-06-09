import re
import logging

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import transaction

from app.models import Group, Student, Teacher
from login.models import PersonalData

User = get_user_model()
logger = logging.getLogger(__name__)

class LogInForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Password'}))

    def clean(self):
        username = self.cleaned_data['username']
        if re.fullmatch(r'\w+@\w+\.\w\w+', username):
            user = User.objects.get(email=username)
            self.cleaned_data['username'] = user.username

        super().clean()


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        label='First Name',
        widget=forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'First Name'}),
    )
    last_name = forms.CharField(
        max_length=30,
        label='Last Name',
        widget=forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Last Name'}),
    )
    email = forms.EmailField(
        max_length=254,
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Email'}),
        error_messages={'unique': 'A user with that email already exists.'},
    )
    username = forms.CharField(
        max_length=150,
        label='Username',
        widget=forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Username'}),
        error_messages={'unique': 'A user with that username already exists.'},
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Password'}),
    )
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Password confirmation'}),
    )
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        label='Group',
        widget=forms.Select(attrs={'class': 'form-control form-control-user'}),
        required=False,
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2', 'group']

    def __init__(self, *args, **kwargs):
        user_type = kwargs.pop('user_type', None)
        super(SignUpForm, self).__init__(*args, **kwargs)

        if user_type == 'teacher':
            self.fields['group'].widget = forms.HiddenInput()

    @transaction.atomic
    def save(self, user_type, commit=True):
        user = super().save(commit=False)
        if user_type == 'student':
            user._student = True
            user.save()
            Student.objects.create(user=user, group=self.cleaned_data['group'])
            PersonalData.objects.create(user=user)
        elif user_type == 'teacher':
            user._teacher = True
            logger.info('User: %s', user)
            user.save()
            Teacher.objects.create(user=user)
            PersonalData.objects.create(user=user)

        return user


class PersonalDataForm(forms.ModelForm):
    phone = forms.CharField(
        max_length=15,
        label='Phone',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
    )
    contact_email = forms.EmailField(
        max_length=254,
        label='Contact Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Contact Email'}),
    )
    telegram = forms.CharField(
        max_length=150,
        label='Telegram',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telegram'}),
    )

    class Meta:
        model = PersonalData
        fields = ['phone', 'contact_email', 'telegram']

    def save(self, commit=True):
        user = self.instance.user
        personal_data = super().save(commit=False)
        personal_data.user = user
        personal_data.save()
        return personal_data
