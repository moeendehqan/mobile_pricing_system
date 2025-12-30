from django.db import models
from utils.storage import CustomS3Storage
from django.conf import settings
# Create your models here.

class transactions(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bede = models.PositiveIntegerField(default=0)
    best = models.PositiveIntegerField(default=0)
    uniqidentifier = models.CharField(max_length=10, null=True, blank=True, verbose_name='شناسه پرداخت')
    transaction_type = models.CharField(max_length=10, choices=[('online', 'انلاین'), ('offline', 'فیش')], default='online')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    document = models.FileField(upload_to='documents/', null=True, blank=True, verbose_name='فیش پرداخت',storage=CustomS3Storage())
    is_confirmed = models.BooleanField(default=False)
    confirm_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - {self.amount}"