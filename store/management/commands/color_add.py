from django.core.management.base import BaseCommand
from store.models import Color



class Command(BaseCommand):
    help = 'Add colors to the database'

    def handle(self, *args, **kwargs):
        colors = [
            {'name': 'سفید', 'hex_code': '#FFFFFF'},
            {'name': 'خاکستری', 'hex_code': '#808080'},
            {'name': 'نقره‌ای', 'hex_code': '#C0C0C0'},
            {'name': 'طلایی', 'hex_code': '#D4AF37'},
            {'name': 'رزگلد', 'hex_code': '#B76E79'},
            {'name': 'قرمز', 'hex_code': '#FF0000'},
            {'name': 'شرابی', 'hex_code': '#800020'},
            {'name': 'نارنجی', 'hex_code': '#FFA500'},
            {'name': 'زرد', 'hex_code': '#FFFF00'},
            {'name': 'سبز', 'hex_code': '#008000'},
            {'name': 'سبز نعنایی', 'hex_code': '#98FF98'},
            {'name': 'سبز زیتونی', 'hex_code': '#808000'},
            {'name': 'آبی', 'hex_code': '#0000FF'},
            {'name': 'آبی آسمانی', 'hex_code': '#87CEEB'},
            {'name': 'آبی نفتی', 'hex_code': '#003366'},
            {'name': 'آبی یخی', 'hex_code': '#E0F7FA'},
            {'name': 'بنفش', 'hex_code': '#800080'},
            {'name': 'یاسی', 'hex_code': '#C8A2C8'},
            {'name': 'فیروزه‌ای', 'hex_code': '#40E0D0'},
            {'name': 'کرم', 'hex_code': '#FFFDD0'},
            {'name': 'بژ', 'hex_code': '#F5F5DC'},
            {'name': 'قهوه‌ای', 'hex_code': '#8B4513'},
            {'name': 'دودی', 'hex_code': '#696969'},
            {'name': 'گرافیت', 'hex_code': '#383838'},
            {'name': 'سرمه‌ای', 'hex_code': '#1A237E'},
            {'name': 'آبی کاربنی', 'hex_code': '#0F4C81'},
            {'name': 'آبی کبالت', 'hex_code': '#0047AB'},
            {'name': 'آبی دریایی', 'hex_code': '#000080'},
            {'name': 'نیلی', 'hex_code': '#4B0082'},
            {'name': 'ارغوانی', 'hex_code': '#800000'},
            {'name': 'بادمجانی', 'hex_code': '#614051'},
            {'name': 'صورتی', 'hex_code': '#FFC0CB'},
            {'name': 'صورتی سیر', 'hex_code': '#FF1493'},
            {'name': 'مرجانی', 'hex_code': '#FF7F50'},
            {'name': 'آجری', 'hex_code': '#B22222'},
            {'name': 'مسی', 'hex_code': '#B87333'},
            {'name': 'عسلی', 'hex_code': '#DAA520'},
            {'name': 'یشمی', 'hex_code': '#00A86B'},
            {'name': 'زغالی', 'hex_code': '#2F2F2F'},
        ]
        for color in colors:
            Color.objects.create(name=color['name'], hex_code=color['hex_code'])
        self.stdout.write(self.style.SUCCESS('Successfully added colors to the database'))