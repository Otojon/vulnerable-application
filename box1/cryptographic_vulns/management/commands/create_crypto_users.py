# cryptographic_vulns/management/commands/create_crypto_users.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from cryptographic_vulns.models import UserProfile

class Command(BaseCommand):
    help = 'Creates users for the cryptographic_vulns app'

    def handle(self, *args, **kwargs):
        # Create user1
        user1, created = User.objects.get_or_create(username='user1')
        if created:
            user1.set_password('password123')
            user1.save()
            UserProfile.objects.create(user=user1, role='normal', flag=None)

        # Create admin user
        admin_user, created = User.objects.get_or_create(username='admin')
        if created:
            admin_user.set_password('adminpass')
            admin_user.save()
            UserProfile.objects.create(user=admin_user, role='admin', flag='flag{test123}')

        print("Users created successfully for cryptographic_vulns app")
