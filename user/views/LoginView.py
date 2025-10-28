from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from user.serializers import LoginInputSerializer
from user.models import Otp
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

User = get_user_model()



class LoginView(APIView):
    permission_classes = [AllowAny]
    @extend_schema(request=LoginInputSerializer,)
    def post(self, request):
        mobile = request.data.get('mobile')
        otp = request.data.get('otp')
        if not mobile or not otp:
            return Response({'message': 'شماره موبایل و کد تایید را وارد کنید'}, status=status.HTTP_400_BAD_REQUEST)
        otp = Otp.objects.filter(mobile=mobile, otp=otp).first()
        if not otp:
            return Response({'message': 'کد تایید اشتباه است'}, status=status.HTTP_400_BAD_REQUEST)
        otp.delete()
        user = User.objects.filter(mobile=mobile).first()

        if not user:
            user = User.objects.create(
                mobile=mobile,
                username=mobile,
            )
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        return Response({'access': access,'refresh': str(refresh)}, status=status.HTTP_200_OK)
