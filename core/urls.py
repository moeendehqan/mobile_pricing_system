


from django.urls import path
from .views import CallbackViewSet

urlpatterns = [
    path('callback/',CallbackViewSet.as_view(),name='callback'),
]
