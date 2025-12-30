from django.core.management.base import BaseCommand
from core.services.zarinpal import ZarinpalService



class Command(BaseCommand):
    def handle(self, *args, **options):
        zarinpal = ZarinpalService()
        # response = zarinpal.create(
        #     amount=100000,
        #     description="test",
        #     mobile="09123456789",
        # )
        response = zarinpal.verify(
            authority="S0000000000000000055500000000000xr7ov",
            amount=100000,
        )
        self.stdout.write(self.style.SUCCESS(f"PaymentRequest: {response}"))
