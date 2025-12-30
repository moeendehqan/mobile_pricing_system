from django.contrib import admin
from .models import transactions


@admin.register(transactions)
class transactionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'id')