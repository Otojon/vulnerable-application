# access_control/management/commands/create_default_users.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from access_control.models import UserProfile

class Command(BaseCommand):
    help = 'Create default users (otojon, abbos, and admin)'

    def handle(self, *args, **kwargs):
        users = [
            {'username': 'otojon', 'password': 'password123', 'role': 'normal'},
            {'username': 'abbos', 'password': 'password123', 'role': 'normal'},
            {'username': 'admin', 'password': 'adminpassword', 'role': 'admin'},
        ]

        for user_data in users:
            user, created = User.objects.get_or_create(username=user_data['username'])
            if created:
                user.set_password(user_data['password'])
                user.save()
                UserProfile.objects.create(user=user, role=user_data['role'])
                self.stdout.write(self.style.SUCCESS(f'User {user.username} created with role {user_data["role"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'User {user.username} already exists'))
