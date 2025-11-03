from rest_framework import serializers
from .models import Product , Order , Picture , ModelMobile, Color, PardNumber
from datetime import timedelta
from django.utils import timezone
from user.serializers import UserSerializer


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id', 'name', 'hex_code']

class PardNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PardNumber
        fields = "__all__"


class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = '__all__'

class MobileSerializer(serializers.ModelSerializer):
    picture = PictureSerializer(many=True)
    colors = ColorSerializer(many=True, read_only=True)

    class Meta:
        model = ModelMobile
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    picture = PictureSerializer(many=True, required=False)
    model_mobile = MobileSerializer(required=False)

    class Meta:
        model = Product
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    picture = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Picture.objects.all(),
        required=False
    )
    model_mobile = serializers.PrimaryKeyRelatedField(
        queryset=ModelMobile.objects.all()
    )


    class Meta:
        model = Product
        fields = "__all__"



class ProductReadSerializer(serializers.ModelSerializer):
    picture = PictureSerializer(many=True, read_only=True)
    model_mobile = MobileSerializer(read_only=True)

    is_available = serializers.SerializerMethodField()
    reversed_to = serializers.SerializerMethodField()

    def get_reversed_to(self, obj):
        # Only consider active reservations (ordering status)
        latest_created_at = (
            Order.objects
            .filter(product=obj, status='ordering')
            .values_list('created_at', flat=True)
            .order_by('-created_at')
            .first()
        )
        if not latest_created_at:
            return None
        to = latest_created_at + timedelta(minutes=10)
        return to if to > timezone.now() else None
                
    def get_is_available(self, obj):
        if self.get_reversed_to(obj):
            return False
        if Order.objects.filter(product=obj, status__in=['approved', 'confirmed']).exists():
            return False
        return True
    class Meta:
        model = Product
        fields = "__all__"



class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    buyer = UserSerializer()
    seller = UserSerializer()
    class Meta:
        model = Order
        fields = "__all__"

class PictureInputSerializer(serializers.Serializer):
    name = serializers.CharField(required=False, allow_blank=True)
    file = serializers.FileField(required=False, allow_null=True)

class ProductInputSerializer(serializers.Serializer):
    name = serializers.CharField(required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
    color = serializers.CharField(required=False, allow_blank=True)
    type_product = serializers.CharField(required=False, allow_blank=True)
    technical_problem = serializers.CharField(required=False, allow_blank=True)
    hit_product = serializers.BooleanField(required=False)
    guarantor = serializers.CharField(required=False, allow_blank=True)
    repaired = serializers.BooleanField(required=False)
    status_product = serializers.CharField(required=False, allow_blank=True)
    picture = PictureInputSerializer(required=False)

class OrderInputSerializer(serializers.Serializer):
    product = ProductInputSerializer(required=False)
    buyer = UserSerializer(required=False)
    seller = UserSerializer(required=False)
    sell_date = serializers.DateField(required=False, allow_null=True)
    status = serializers.CharField(required=False, allow_blank=True)


class MobileInputSerializer(serializers.Serializer):
    model_name = serializers.CharField(required=False, allow_blank=True)
    color = serializers.CharField(required=False, allow_blank=True)
    picture = PictureInputSerializer(required=False)
    is_apple = serializers.BooleanField(required=False)
    part_number = serializers.CharField(required=False, allow_blank=True)
    registered = serializers.BooleanField(required=False)
    link = serializers.URLField(required=False, allow_blank=True)

