from django.db import models
from user.models import User
from colorfield.fields import ColorField




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
    file = models.FileField(
        upload_to=('product/picture/'),
        null=True,
        blank=True,
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
        if self.model_mobile:
            return f"{self.model_mobile.brand} {self.model_mobile.model_name} - {self.seller.username if self.seller else 'بدون فروشنده'}"
        return f"محصول {self.id}"


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
        if self.colors.count() == 0:
            self.colors.add(Color.objects.all())
        super().save(*args, **kwargs)

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


    class Meta:
        verbose_name = ("محصول")
        verbose_name_plural = ("محصولات")
        permissions = [('can_create_products','می تواند محصولات را ایجاد کند'),('can_update_products','می تواند محصولات را بروزرسانی کند'),('can_delete_products','می تواند محصولات را حذف کند')]
        ordering = ['-seller__vip_sort','-created_at']
    def __str__(self):
        return f"{self.id} - {self.model_mobile.model_name} - {self.price}"

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
