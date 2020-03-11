from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, department, password=None, commit=True):
        """
        Creates and saves a User with the given email, first name, last name and
        password.
        """
        if not email:
            raise ValueError(_('Users must have an email address'))
        if not first_name:
            raise ValueError(_('Users must have a first name'))
        if not last_name:
            raise ValueError(_('Users must have a last name'))
        if not department:
            raise ValueError(_('Users must have a department'))

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            department=department,
            is_active=True,
            is_staff=False,
            is_superuser=False,
            date_joined=timezone.now()
        )
        user.set_password(password)
        if commit:
            user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, department, password):
        """
        Creates and save a superuser with the given email, first name, last name
        and password
        """
        user = self.create_user(
            email,
            first_name,
            last_name,
            department,
            password,
            commit=False,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):

    IT = 1
    Admin = 2
    HR = 3
    Maintenance = 4
    DEPARTMENT_CHOICES = (
        (IT, _('IT')),
        (Admin, _('Admin')),
        (HR, _('HR')),
        (Maintenance, _('Maintenance')),
    )

    email = models.EmailField(
        verbose_name=_('email address'), max_length=100, unique=True
    )
    first_name = models.CharField(_('first name'), max_length=30, blank=False)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    department = models.IntegerField(_('department'), choices=DEPARTMENT_CHOICES, blank=False)
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'
        ),
    )
    date_joined = models.DateTimeField(
        _('date joined'),
        default=timezone.now
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'department']

    def get_full_name(self):
        return (self.first_name + " " + self.last_name).strip()

    def get_email(self):
        return str(self.email)

    def __str__(self):
        return self.get_full_name() + " " + self.get_email()

