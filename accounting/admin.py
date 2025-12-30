from django.contrib import admin

# Register your models here.

@admin.register(transactions)
class transactionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'id')