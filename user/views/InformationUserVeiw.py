from rest_framework.permissions import IsAuthenticated
from rest_framework import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserSerializer
from .models import User



class InformationUserView(APIView):
    permission_classes = [IsAuthenticated]
    def get (self, request,id=None):
        user = request.user
        if not user.admin:
            return Response({'error': 'دسترسی غیرمجاز'}, status=status.HTTP_403_FORBIDDEN)
        if id == None:
            if not user.has_perm('user.can_see_all_users'):
                return Response({'error': 'دسترسی غیرمجاز'}, status=status.HTTP_403_FORBIDDEN)
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        user = User.objects.filter(id=id).first()
        if not user:
            return Response({'error': 'کاربر یافت نشد'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)