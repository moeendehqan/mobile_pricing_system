from django.shortcuts import render

# Create your views here.
class CallbackViewSet(APIView):
    permission_classes = [AllowAny]
    def post (self,request):
        return Response({"message":"callback"})
    def get (self,request):
        return Response({"message":"callback"})