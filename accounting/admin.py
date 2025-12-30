from django.contrib import admin
from .models import transactions


@admin.register(transactions)
class transactionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'bede', 'best', 'confirm_at', 'created_at')
    list_filter = ('transaction_type', 'created_at')
    search_fields = ('user__username', 'id')