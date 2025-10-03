from datetime import timedelta
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone
from blango_auth.models import User

class Command(BaseCommand):
    help = "Delete users that registered but did not activate within ACCOUNT_ACTIVATION_DAYS"

    def handle(self, *args, **kwargs):
        cutoff = timezone.now() - timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)
        deleted, _ = User.objects.filter(
            is_active=False,
            date_joined__lt=cutoff
        ).delete()

        self.stdout.write(self.style.SUCCESS(f"Deleted {deleted} inactive users"))
