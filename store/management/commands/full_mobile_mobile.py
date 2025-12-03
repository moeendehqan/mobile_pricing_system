from django.core.management.base import BaseCommand
from store.models import ModelMobile, Picture
import pandas as pd
import requests
from django.core.files.base import ContentFile
from django.db import transaction


BATCH_SIZE = 500   # تعداد رکوردهایی که هر بار bulk ذخیره شوند


class Command(BaseCommand):
    help = "Fast import mobile models + pictures without saving URLs"

    def handle(self, *args, **kwargs):
        df = pd.read_csv('phone_dataset.csv', on_bad_lines='skip')
        df = df[1630:]

        mobiles_to_create = []
        created_objects = []

        # ======================================
        # مرحله ۱ — آماده‌سازی رکوردها در حافظه
        # ======================================
        for index, row in df.iterrows():

            model_name = row['model']
            brand = row['brand']
            is_apple = (brand == 'Apple')

            # اگر موبایل موجود باشد، skip
            if ModelMobile.objects.filter(model_name=model_name).exists():
                continue

            mobiles_to_create.append(
                ModelMobile(
                    model_name=model_name,
                    brand=brand,
                    is_apple=is_apple,
                )
            )

            # اگر تعداد به حد batch رسید، ذخیره کن
            if len(mobiles_to_create) >= BATCH_SIZE:
                created = ModelMobile.objects.bulk_create(mobiles_to_create)
                created_objects.extend(created)
                mobiles_to_create = []

        # ذخیره باقی‌مانده‌ها
        if mobiles_to_create:
            created = ModelMobile.objects.bulk_create(mobiles_to_create)
            created_objects.extend(created)

        self.stdout.write(self.style.SUCCESS(f"{len(created_objects)} mobiles imported."))

        # ======================================
        # مرحله ۲ — دانلود عکس و اضافه کردن به Picture
        # ======================================
        for mobile in created_objects:

            img_url = df.loc[df['model'] == mobile.model_name, 'img_url'].values[0]

            if not isinstance(img_url, str) or not img_url.startswith("http"):
                continue

            try:
                response = requests.get(img_url, timeout=10)
                if response.status_code == 200:
                    pic = Picture.objects.create(name=mobile.model_name)
                    pic.file.save(
                        f"{mobile.model_name}.jpg",
                        ContentFile(response.content)
                    )
                    mobile.picture.add(pic)
            except:
                print(f"❌ Failed to download: {img_url}")

        self.stdout.write(self.style.SUCCESS("Pictures imported successfully"))
