from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from utils.message import MessageMelipayamak
from .serializers import OtpInputSerializer
from .models import Otp
import random



class OtpView(APIView):
    permission_classes = [AllowAny]
    @extend_schema(request=OtpInputSerializer,)
    def post(self, request):
        mobile = request.data.get('mobile')
        if not mobile:
            return Response({'message': 'شماره موبایل را وارد کنید'}, status=status.HTTP_400_BAD_REQUEST)
        otp = random.randint(100000, 999999)
        MessageMelipayamak().otpSMS(otp,mobile)
        otp = Otp.objects.create(mobile=mobile, otp=otp)
        return Response({'message': 'کد تایید به شماره موبایل شما ارسال شد'}, status=status.HTTP_200_OK)
