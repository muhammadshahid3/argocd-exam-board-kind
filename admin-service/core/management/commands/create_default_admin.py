from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Creates the default admin superuser for local development if it does not already exist."

    def handle(self, *args, **options):
        User = get_user_model()
        username = settings.DEFAULT_ADMIN_USERNAME
        password = settings.DEFAULT_ADMIN_PASSWORD
        email = settings.DEFAULT_ADMIN_EMAIL

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f"Admin user '{username}' already exists. Skipping."))
            return

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f"Default admin user '{username}' created."))
