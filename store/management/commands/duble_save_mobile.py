from django.core.management.base import BaseCommand
from store.models import ModelMobile, Color


class Command(BaseCommand):
    help = 'Double save mobiles'
    
    def handle(self, *args, **kwargs):
        mobiles = ModelMobile.objects.all()
        colors = Color.objects.all()
        len_mobiles = len(mobiles)
        for index, mobile in enumerate(mobiles):
            rate = ((index+1) / len_mobiles) * 100
            rate = round(rate, 2)
            mobile.colors.add(*colors)
            mobile.save()
            self.stdout.write(self.style.SUCCESS(f"{rate} {mobile.model_name} saved."))
