from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from user.serializers import UserSerializer
from user.models import User
from drf_spectacular.utils import extend_schema
 


class UserUpdateView(APIView):
    permission_classes=[IsAuthenticated]
    @extend_schema(request=UserInputSerializer)
    def patch(self,request,id):
        if not request.user.has_perm('user.can_see_all_users'):
            return Response({'message': 'دسترسی غیرمجاز'}, status=status.HTTP_403_FORBIDDEN)
        user = User.objects.filter(id=id).first()
        if not user:
            return Response({'message': 'کاربر یافت نشد'}, status=status.HTTP_404_NOT_FOUND)
        request.data['password'] = 'defualt'
        serializer = UserSerializer(user, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response ({'message' : 'اطلاعات کاربر با موفقیت به روز شد'}, status=status.HTTP_200_OK)


class RefreshView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        refresh = RefreshToken(request.data.get('refresh'))
        access = str(refresh.access_token)
        return Response({'access': access}, status=status.HTTP_200_OK)