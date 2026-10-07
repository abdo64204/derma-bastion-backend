import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create default superuser if none exists (username: admin, default password: adminpassword or via env)"

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@dermabastion.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123456')

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' created successfully! (Password: {password})"))
        else:
            self.stdout.write(f"Superuser '{username}' already exists.")
