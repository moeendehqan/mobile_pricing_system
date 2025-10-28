from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from user.serializers import UserSerializer, ProfileUpdateSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema



class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    @extend_schema(request=ProfileUpdateSerializer, responses=UserSerializer)
    def patch(self, request, *args, **kwargs):
        user = request.user
        serializer = ProfileUpdateSerializer(user, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
    
