from django.db import models
import uuid
from django.contrib.postgres.fields import ArrayField
# Create your models here.

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have a email')

        user = self.model(username=username, email=self.normalize_email(email))

        user.set_password(password)
        user.save()
        return user

    def create_super_user(self, username, email, password=None):
        if password is None:
            raise TypeError('Users should have a password')
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


AUTH_PROVIDERS = {
    'facebook': 'facebook',
    'google': 'google',
    'twitter': 'twitter',
    'email': 'email'

}


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        max_length=255
    )
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)
    email = models.EmailField(unique=True, null=False)
    username = models.CharField(max_length=255, unique=True, null=False)
    date_of_birth = models.DateField(null=True)
    about = models.TextField()
    auth_provider = models.CharField(max_length=300,
                                     blank=False,
                                     null=False,
                                     default=AUTH_PROVIDERS.get('email'))

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    host_reviews = ArrayField(models.JSONField(null=False), null=True)
    host_rating = models.FloatField(default=0)
    interests = ArrayField(models.TextField(), null=True)
    events_attended = ArrayField(models.JSONField(null=False), null=True)
    events_hosted = ArrayField(models.JSONField(null=False), null=True)
    password = models.CharField(max_length=255, null=False)
    social_accounts = models.JSONField(null=True)
    first_timer = models.BooleanField(default=True)
    account_blocked = models.BooleanField(default=False)
    deactivated_account = models.BooleanField(default=False)
    profile_picture = models.URLField()
    event_highlights = ArrayField(models.JSONField(null=False), null=True)
    following = ArrayField(models.CharField(max_length=50), null=True)
    followers = ArrayField(models.CharField(max_length=50), null=True)
    notification = ArrayField(models.JSONField(null=False), null=True)
    user_logs = ArrayField(models.JSONField(null=False), null=True)
    calender = ArrayField(models.JSONField(null=False), null=True)
    analytics = models.JSONField(null=True)
    date_joined = models.DateField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name',
                       'last_name', 'date_of_birth', 'gender']

    objects = UserManager()

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    def __str__(self):
        return self.username


# class Agency(models.Model):
#   id = models.UUIDField(
#       primary_key=True,
#       default=uuid.uuid4,
#       editable=False
#   )
#   agency_name = models.CharField(max_length=128)
#   members = models.ManyToManyField(User, through='Membership')
#   contact = models.JSONField(null=True)
#   events_hosted = ArrayField(models.JSONField(null=False), null=True)
#   events_attended = ArrayField(models.JSONField(null=False), null=True)
#   about = models.TextField(default='')
#   event_types = ArrayField(models.TextField(), null=True)
#   host_reviews = ArrayField(models.JSONField(null=False), null=True)
#   host_rating = models.FloatField(default=0)
#   analytics = models.JSONField(null=True)
#   following = ArrayField(models.CharField(max_length=50), null=True)
#   followers = ArrayField(models.CharField(max_length=50), null=True)
#   social_accounts = models.JSONField(null=True)
#   profile_picture = models.URLField()
#   event_highlights = ArrayField(models.JSONField(null=False))
#   notification = ArrayField(models.JSONField(null=False), null=True)
#   user_logs = ArrayField(models.JSONField(null=False), null=True)
#   calender = ArrayField(models.JSONField(null=False), null=True)
#   account_blocked = models.BooleanField(default=False)
#   deactivated_account = models.BooleanField(default=False)

#   def __str__(self):
#     return self.id


# class Membership(models.Model):
#   user = models.ForeignKey(User, on_delete=models.CASCADE)
#   agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
#   AGENCY_ROLES = (
#       ('A', 'Admin'),
#       ('R', 'Regular')
#   )
#   role = models.CharField(max_length=1, choices=AGENCY_ROLES, default='R')
#   date_joined = models.DateField(auto_now=True)
