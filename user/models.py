from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from utils.storage import CustomS3Storage
import uuid
import os

class User(AbstractUser):
    def _user_picture_upload_to(self, filename):
        ext = os.path.splitext(filename)[1]
        return f"user/picture/{uuid.uuid4().hex}{ext}"
    username = models.CharField(
        max_length=255,
        unique=True,

        verbose_name='کاربر')

    uniqidentifier = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='کدملی')

    first_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='نام')

    last_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='نام خانوادگی')

    email = models.EmailField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='ایمیل')

    mobile = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='تلفن')

    address = models.TextField(
        null=True,
        blank=True,
        verbose_name='آدرس')

    city = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='شهر')

    company = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='نام شرکت')

    sheba_number = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='شماره شبا')

    card_number = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='شماره کارت')

    account_number = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='شماره حساب')

    account_bank = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='نام بانک')

    is_verified = models.BooleanField(
        default=False,
        verbose_name='احراز هویت شده')

    admin = models.BooleanField(
        default=False,
        verbose_name='ادمین')

    work_guarantee = models.BooleanField(
        default=False,
        verbose_name='ضمانت نامه حسن انجام کار')

    is_active = models.BooleanField(
        default=True,
        verbose_name='فعال')

    is_register = models.BooleanField(
        default=False,
        verbose_name='ثبت نام شده')

    created_at = models.DateTimeField(
        auto_now_add=True)

    updated_at = models.DateTimeField(
        auto_now=True)
    business_license = models.ImageField(
        upload_to=_user_picture_upload_to,
        null=True,
        blank=True,
        storage=CustomS3Storage(),
        verbose_name='جواز کسب و کار')
    head_store_image = models.ImageField(
        upload_to=_user_picture_upload_to,
        null=True,
        blank=True,
        storage=CustomS3Storage(),  
        verbose_name='تصویر تابلو فروشگاه')
    store_window_image = models.ImageField(
        upload_to=_user_picture_upload_to,
        null=True,
        blank=True,
        storage=CustomS3Storage(),
        verbose_name='تصویر ویترین فروشگاه')
    Warranty_check_image = models.ImageField(
        upload_to=_user_picture_upload_to,
        null=True,
        blank=True,
        storage=CustomS3Storage(),
        verbose_name='تصویر چک ضمانت')
    vip_sort = models.IntegerField(
        default=0,
        verbose_name='رتبه وی ای پی')


    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'
        permissions = [('can_see_all_users','می تواند همه کاربران را ببیند')]

    def __str__(self):
        return f"{self.username}"
    def clean(self):
        super().clean()
        if self.uniqidentifier:
            exists = User.objects.exclude(pk=self.pk).filter(uniqidentifier=self.uniqidentifier).exists()
            if exists:
                raise ValidationError({'uniqidentifier': 'این کد ملی قبلاً استفاده شده است.'})



class Otp(models.Model):
    mobile = models.CharField(max_length=255)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'کد یکبار مصرف'
        verbose_name_plural = 'کد های یکبار مصرف'

    def __str__(self):
        return f"{self.mobile} - {self.otp}"