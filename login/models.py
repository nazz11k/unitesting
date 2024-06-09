from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password, first_name, last_name, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.set_first_name(first_name)
        user.set_last_name(last_name)
        user.save()
        return user

    def create_teacher(self, username, email, password, first_name, last_name):
        user = self.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        user.staff = True
        user._teacher = True
        user.save()
        return user

    def create_student(self, username, email, password, first_name, last_name):
        user = self.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        user._student = True
        user.staff = True
        user.save()
        return user

    def create_superuser(self, username, email, password, first_name, last_name):
        user = self.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        user.staff = True
        user.admin = True
        user.save()
        return user


class User(AbstractUser):
    email = models.EmailField(verbose_name='email', unique=True)
    username = models.CharField(verbose_name='username', max_length=150, unique=True)
    first_name = models.CharField(verbose_name='first name', max_length=150, unique=True)
    last_name = models.CharField(verbose_name='last name', max_length=150, unique=True)
    _student = models.BooleanField(default=False)
    _teacher = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    objects = CustomUserManager()

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name

    def get_email(self):
        return self.email

    def get_username(self):
        return self.username

    def set_first_name(self, first_name):
        self.first_name = first_name

    def set_last_name(self, last_name):
        self.last_name = last_name

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_student(self):
        return self._student

    @property
    def is_teacher(self):
        return self._teacher


class PersonalData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    telegram = models.CharField(max_length=50, blank=True, null=True)

    def set_phone(self, phone):
        self.phone = phone

    def set_contact_email(self, contact_email):
        self.contact_email = contact_email

    def set_telegram(self, telegram):
        self.telegram = telegram

    def get_phone(self):
        return self.phone

    def get_contact_email(self):
        return self.contact_email

    def get_telegram(self):
        return self.telegram
