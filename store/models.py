from django.db import models
from django.db.models.signals import m2m_changed
from colorfield.fields import ColorField
from utils.telegram import Telegram
from utils.storage import CustomS3Storage
import os
import uuid
import html
from django.contrib.auth import get_user_model


User = get_user_model()



class Color(models.Model):
    name = models.CharField(
        max_length=128,
        verbose_name='نام رنگ',
        unique=True
    )
    hex_code = ColorField(default='#FF0000')

    class Meta:
        verbose_name = ("رنگ")
        verbose_name_plural = ("رنگ ها")

    def __str__(self):
        return self.name


class PardNumber (models.Model):
    pard_number = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='پارت نمبر'
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='توضیحات'
    )
    created_at = models.DateTimeField(
        auto_now_add=True)

    updated_at = models.DateTimeField(
        auto_now=True)

    class Meta:
        verbose_name = ("پارت نامبر")
        verbose_name_plural = ("پارت نامبر ها")

class Picture (models.Model):
    def _product_picture_upload_to(self, filename):
        ext = os.path.splitext(filename)[1]
        return f"product/picture/{uuid.uuid4().hex}{ext}"

    file = models.FileField(
        upload_to=_product_picture_upload_to,
        null=True,
        blank=True,
        storage=CustomS3Storage(),
        verbose_name='تصویر'
    )

    name =  models.CharField(
        max_length=255,
        null= True,
        blank= True,
        verbose_name='نام تصویر')

    created_at = models.DateTimeField(
        auto_now_add=True)

    updated_at = models.DateTimeField(
        auto_now=True)

    class Meta:
        verbose_name = ("تصویر")
        verbose_name_plural = ("تصاویر")

    def __str__(self):
        return self.name or f"تصویر {self.id}"



class ModelMobile (models.Model):
    model_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='نام مدل'
    )

    brand = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='برند'
    )

    colors = models.ManyToManyField(
        Color,
        blank=True,
        related_name='mobile_colors',
        verbose_name='رنگ‌ها',
    )
    
    picture = models.ManyToManyField(
        Picture,
        blank=True,
        related_name='mobile_picture',
        verbose_name='تصاویر'
    )

    is_apple = models.BooleanField(
        default=False,
        verbose_name='اپل'
    )

    link = models.URLField(
        null=True,
        blank=True,
        verbose_name='لینک'
    )
    link_2 = models.URLField(
        null=True,
        blank=True,
        verbose_name='لینک دوم'
    )
    link_3 = models.URLField(
        null=True,
        blank=True,
        verbose_name='لینک سوم'
    )
    link_4 = models.URLField(
        null=True,
        blank=True,
        verbose_name='لینک  چهارم'
    )
    link_5 = models.URLField(
        null=True,
        blank=True,
        verbose_name='لینک  پنجم'
    )

    created_at = models.DateTimeField(
        auto_now_add=True)

    updated_at = models.DateTimeField(
        auto_now=True)

    class Meta:
        verbose_name = ("موبایل")
        verbose_name_plural = ("موبایل ها")
    def save(self, *args, **kwargs):
        if self.is_apple:
            self.brand = 'اپل'
        creating = self.pk is None
        # Save first to ensure we have a PK before touching M2M relations
        super().save(*args, **kwargs)
        # On initial create, if no colors were provided, default to all colors
        if creating and self.colors.count() == 0:
            self.colors.set(Color.objects.all())

    def __str__(self):
        return self.model_name

class Product (models.Model):
    seller = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name='product_seller',
        verbose_name='فروشنده'
    )
    registered = models.BooleanField(
        default=True,
        verbose_name=' رجیستر شده'
    )
    charge_cicle = models.PositiveIntegerField(
        default=0,
        verbose_name='میزان شارژ هر دوره')

    description = models.TextField(
        null= True,
        blank= True,
        verbose_name='توضیحات')
    
    description_appearance = models.TextField(
        null= True,
        blank= True,
        verbose_name='توضیحات ظاهر')
    
    technical_problem = models.TextField(
        null= True,
        blank= True,
        verbose_name='توضیحات مشکل فنی')

    price = models.BigIntegerField(
        null= True,
        blank= True,
        verbose_name='قیمت')
    
    customer_price = models.BigIntegerField(
        default=0,
        verbose_name='قیمت مشتری')

    color =models.ForeignKey(Color,on_delete=models.SET_NULL , null=True, verbose_name='رنگ')

    picture = models.ManyToManyField(
        Picture,
        blank=True,
        null=True,
        related_name='product_picture',
        verbose_name='تصاویر'
    )

    battry_health =models.IntegerField(default=100,verbose_name='سلامت باتری')

    battry_change =models.BooleanField (
        default= False,
        verbose_name='باتری تعویض شده'
    )

    TYPE_PRODUCT = [
        ('new','نو'),
        ('as new','در حد نو'),
        ('used','دست دوم'),
    ]

    type_product =models.CharField(
        max_length=25,
        default="used",
        choices=TYPE_PRODUCT,
        null= True,
        blank= True,
        verbose_name='وضعیت محصول')
    
    auction = models.BooleanField (
        default= False,
        verbose_name='مزایده'
    )

    guarantor = models.IntegerField(
        default=0,
        verbose_name='گارانتی ماه')

    repaired = models.BooleanField (
        default= False,
        verbose_name='تعمیر شده'
    )
    part_num = models.CharField(
        max_length=258,
        null= True,
        blank= True,
        verbose_name='پارت نامبر')

    STATUS_PRODUCT =[
        ('open','باز'),
        ('saled','فروخته شده'),
        ('canseled','کنسل شده'),
        ('reserved','رزرو'),
    ]
    status_product = models.CharField(
        max_length=25,
        choices=STATUS_PRODUCT,
        default='open',
        verbose_name='وضعیت فروش محصول')

    CARTON = [
        ('orginal','اورجینال'),
        ('repakage','رپیکیج'),
    ]
    carton = models.CharField(
        max_length=20,
        choices=CARTON,
        null=True,
        blank=True,
        verbose_name='جعبه'
    )

    GRADE = [
        ('A','در حد نو'),
        ('B','خط و خش جزئی'),
        ('C','خط و خش و ضربه جزئی'),
        ('D','نیاز به تعمیر'),
    ]

    grade = models.CharField(
        max_length=256,
        choices=GRADE,
        default="A",
        null= True,
        blank= True,
        verbose_name='درجه'
    )

    model_mobile = models.ForeignKey(
        ModelMobile,
        null=True,
        on_delete=models.SET_NULL,
        related_name='product_model_mobile',
        verbose_name='مدل موبایل'
    )

    created_at = models.DateTimeField(
        auto_now_add=True)

    updated_at = models.DateTimeField(
        auto_now=True)

    telegram_message_id = models.BigIntegerField(
        null=True,
        blank=True,
        verbose_name='شناسه پیام تلگرام'
    )

    telegram_has_photo = models.BooleanField(
        default=False,
        verbose_name='پیام تصویری'
    )


    class Meta:
        verbose_name = ("محصول")
        verbose_name_plural = ("محصولات")
        permissions = [('can_create_products','می تواند محصولات را ایجاد کند'),('can_update_products','می تواند محصولات را بروزرسانی کند'),('can_delete_products','می تواند محصولات را حذف کند')]
        ordering = ['-seller__vip_sort','-created_at']
    def __str__(self):
        return f"{self.id} - {self.model_mobile.model_name} - {self.price}"
    def send_channel(self):
        telegram = Telegram()
        chat_id = telegram.chat_id_channel
        text = self.build_intro_message()
        first_picture = self.picture.first()
        image_url = None
        if first_picture and getattr(first_picture, 'file', None):
            try:
                image_url = first_picture.file.url
            except Exception:
                image_url = None

        if self.telegram_message_id:
            if self.telegram_has_photo:
                if image_url:
                    telegram.edit_message_media(chat_id, self.telegram_message_id, image_url, text)
                else:
                    telegram.edit_message_caption(chat_id, self.telegram_message_id, text)
            else:
                telegram.edit_message_text(chat_id, self.telegram_message_id, text)
        else:
            if image_url:
                resp = telegram.send_photo(chat_id, image_url, text)
                self.telegram_message_id = (resp.get('result') or {}).get('message_id')
                self.telegram_has_photo = True
                Product.objects.filter(pk=self.pk).update(
                    telegram_message_id=self.telegram_message_id,
                    telegram_has_photo=self.telegram_has_photo
                )
            else:
                resp = telegram.send_message(chat_id, text)
                self.telegram_message_id = (resp.get('result') or {}).get('message_id')
                self.telegram_has_photo = False
                Product.objects.filter(pk=self.pk).update(
                    telegram_message_id=self.telegram_message_id,
                    telegram_has_photo=self.telegram_has_photo
                )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.send_channel()

    def build_intro_message(self):
        escape = html.escape
        brand = escape(self.model_mobile.brand) if (self.model_mobile and self.model_mobile.brand) else None
        model_name = escape(self.model_mobile.model_name) if self.model_mobile else None
        title_text = " ".join([x for x in [brand, model_name] if x]) or "محصول"
        title = f"<b>📱 {title_text}</b>"

        type_disp = escape(self.get_type_product_display()) if self.type_product else None
        grade_disp = escape(self.get_grade_display()) if self.grade else None
        status_line = None
        if type_disp or grade_disp:
            parts = []
            if type_disp:
                parts.append(f"<b>🎯 وضعیت:</b> {type_disp}")
            if grade_disp:
                parts.append(f"<b>🔖 درجه:</b> {grade_disp}")
            status_line = " | ".join(parts)

        color_line = f"<b>🎨 رنگ:</b> {escape(self.color.name)}" if self.color else None
        battery_line = f"<b>🔋 باتری:</b> {self.battry_health}%" + (" (تعویض شده)" if self.battry_change else "")
        guarantor_line = f"<b>🛡️ گارانتی:</b> {self.guarantor} ماه" if self.guarantor else "<b>🛡️ گارانتی:</b> ندارد"
        carton_disp = escape(self.get_carton_display()) if self.carton else None
        carton_line = f"<b>🧰 جعبه:</b> {carton_disp}" if carton_disp else None
        repaired_line = f"<b>🛠️ تعمیر شده:</b> {'بله' if self.repaired else 'خیر'}"
        auction_line = f"<b>🏷️ مزایده:</b> {'بله' if self.auction else 'خیر'}"
        status_product_disp = escape(self.get_status_product_display()) if self.status_product else None
        status_product_line = f"<b>📦 وضعیت فروش:</b> {status_product_disp}" if status_product_disp else None
        price_line = f"<b>💰 قیمت:</b> {self.price:,} تومان" if self.price else "<b>💰 قیمت:</b> نامشخص"
        part_line = f"<b>🧩 پارت نامبر:</b> {escape(self.part_num)}" if self.part_num else None
        seller_line = None
        if self.seller:
            masked = self._mask_text(self.seller.username, show_start=2, show_end=1)
            seller_line = f"<b>👤 فروشنده:</b> {escape(masked)} (شناسه: {self.seller.id})"

        lines = [
            title,
            price_line,
            status_line,
            color_line,
            battery_line,
            guarantor_line,
            carton_line,
            repaired_line,
            auction_line,
            status_product_line,
            part_line,
            seller_line,
        ]

        if self.description:
            lines.append(f"<b>📝 توضیحات:</b> {escape(self.description)}")
        if self.description_appearance:
            lines.append(f"<b>✨ ظاهر:</b> {escape(self.description_appearance)}")
        if self.technical_problem:
            lines.append(f"<b>⚙️ مشکل فنی:</b> {escape(self.technical_problem)}")

        return "\n".join([l for l in lines if l])

    def _mask_text(self, text, show_start=2, show_end=1, mask_char='*'):
        if not text:
            return ''
        try:
            n = len(text)
        except Exception:
            return ''
        tail_len = show_end if show_end and show_end > 0 else 0
        if n <= show_start + tail_len:
            return mask_char * n
        head = text[:show_start]
        tail = text[-tail_len:] if tail_len > 0 else ''
        masked_mid = mask_char * (n - show_start - tail_len)
        return head + masked_mid + tail


def _product_pictures_changed(sender, instance, action, **kwargs):
    if action in ("post_add", "post_remove", "post_clear"):
        instance.send_channel()

m2m_changed.connect(_product_pictures_changed, sender=Product.picture.through)

class Order (models.Model) :
    product = models.ForeignKey(
        Product,
        null=True,
        on_delete=models.SET_NULL,
        related_name='order_product',
        verbose_name='محصول'
    )

    buyer = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name='order_buyer',
        verbose_name='خریدار'
    )

    seller = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name='order_seller',
        verbose_name='فروشنده'
    )

    sell_date =models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='تاریخ فروش'
    )

    STATUS =[
        ('approved','تکمیل سفارش'),
        ('confirmed','تایید سفارش'),
        ('ordering','در حال سفارش'),
        ('canceled','کنسل شده'),
    ]
    status =models.CharField(
        max_length=25,
        choices=STATUS,
        null= True,
        blank= True,
        verbose_name='وضعیت سفارش')

    created_at = models.DateTimeField(
        auto_now_add=True)

    updated_at = models.DateTimeField(
        auto_now=True)


    class Meta:
        verbose_name = ("سفارش")
        verbose_name_plural = ("سفارشات")
        permissions = [('can_see_all_orders','می تواند همه سفارشات را ببیند') , ('can_update_order','می تواند سفارشات را بروزرسانی کند')]

    def __str__(self):
        return f"Order: {self.product.name} by {self.buyer.username} from {self.seller.username}"
