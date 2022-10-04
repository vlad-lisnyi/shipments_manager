from django.shortcuts import render
from shipments.models import Shipment
from shipments.serializers import ShipmentSerializer

from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class ShipmentViewSet(viewsets.ModelViewSet):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer

