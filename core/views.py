from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny



# Create your views here.
class CallbackViewSet(APIView):
    permission_classes = [AllowAny]
    def post (self,request):
        return Response({"message":"callback"})
    def get (self,request):
        return Response({"message":"callback"})