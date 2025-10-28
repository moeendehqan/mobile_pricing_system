from rest_framework.permissions import IsAuthenticated
from rest_framework import Response
from rest_framework import status
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from .serializers import UserInputSerializer
from .models import User



class RegisterView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(request=UserInputSerializer)
    def post(self, request):
        user = request.user
        if user.is_register:
            return Response({'message': 'قبلا ثبت نام کردید'}, status=status.HTTP_400_BAD_REQUEST)
        User.objects.filter(id=user.id).update(
            mobile=user.mobile,
            username = request.data.get('uniqidentifier'),
            uniqidentifier = request.data.get('uniqidentifier'),
            first_name = request.data.get('first_name'),
            last_name = request.data.get('last_name'),
            email = request.data.get('email'),
            company = request.data.get('company'),
            sheba_number = request.data.get('sheba_number'),
            card_number = request.data.get('card_number'),
            account_number = request.data.get('account_number'),
            account_bank = request.data.get('account_bank'),
            address = request.data.get('address'),
            city = request.data.get('city'),
            is_register = True,
        )

        return Response({'message': 'اطلاعات شما ثبت شد'}, status=status.HTTP_200_OK)
