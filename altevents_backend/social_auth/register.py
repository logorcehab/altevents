from django.contrib.auth import authenticate
from authentication.models import User
import os
import random
from rest_framework.exceptions import AuthenticationFailed


def generate_username(name):

    username = "".join(name.split(' ')).lower()
    if not User.objects.filter(username=username).exists():
        return username
    else:
        random_username = username + str(random.randint(0, 1000))
        return generate_username(random_username)


"""
 Register Users who user social accounts with their id, email  and name 
"""


def register_social_user(provider, user_id, email, last_name, first_name):
    filtered_user_by_email = User.objects.filter(email=email)

    """
        Check if user already exists
    """
    if filtered_user_by_email.exists():
        # Check if the users current provider is the same provider used to register if so Log user in
        if provider == filtered_user_by_email[0].auth_provider:

            registered_user = authenticate(
                email=email, password='SOCIAL_SECRET')
            if registered_user:
                return {
                    'username': registered_user.username,
                    'email': registered_user.email,
                    'tokens': registered_user.tokens()}
        # If provider is not the same return an error and promp user to log in with their initial auth provider
        else:
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)
    # If user does not exits generate usernamme for user and register user
    else:
        user = {
            'username': generate_username(first_name+" "+last_name), 'email': email,
            'password': 'SOCIAL_SECRET'}
        user = User.objects.create_user(**user)
        user.is_verified = True
        user.auth_provider = provider
        user.save()

        new_user = authenticate(
            email=email, password='SOCIAL_SECRET')
        if new_user:
            return {
                'email': new_user.email,
                'username': new_user.username,
                'tokens': new_user.tokens()
            }
