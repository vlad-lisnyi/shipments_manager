from rest_framework import status
import json

from rest_framework.test import force_authenticate
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from shipments.models import Shipment
from shipments.serializers import ShipmentSerializer
from shipments.views import ShipmentViewSet

# Create your tests here.
class TestShipments(TestCase):
    @classmethod
    def setUpTestData(cls):
        Shipment.objects.create(departureLocation="Warsaw", destinationLocation="Krakow")
        Shipment.objects.create(departureLocation="Madrid", destinationLocation="Rome", status=Shipment.COMPLETED)
        Shipment.objects.create(departureLocation="Lodz", destinationLocation="New York", status=Shipment.DELAYED)
        Shipment.objects.create(departureLocation="Krakow", destinationLocation="New York")

    def test_location_fields(self):
        shipment = Shipment.objects.get(departureLocation="Warsaw")
        self.assertTrue(len(shipment.departureLocation) <= 200)
        self.assertTrue(len(shipment.destinationLocation) <= 200)
        
        shipment = Shipment.objects.get(departureLocation="Krakow")
        self.assertTrue(len(shipment.departureLocation) <= 200)
        self.assertTrue(len(shipment.destinationLocation) <= 200)

    def test_status_fields(self):
        shipment = Shipment.objects.get(departureLocation="Warsaw")
        self.assertTrue(shipment.status == Shipment.IN_PROGRESS or shipment.status == Shipment.COMPLETED or shipment.status == Shipment.DELAYED)

class GetAllShipmentsTest(TestCase):
    """ Test module for GET all shipments API """
    @classmethod
    def setUpTestData(cls):
        Shipment.objects.create(departureLocation="Warsaw", destinationLocation="Krakow")
        Shipment.objects.create(departureLocation="Madrid", destinationLocation="Rome", status=Shipment.COMPLETED)
        Shipment.objects.create(departureLocation="Lodz", destinationLocation="New York", status=Shipment.DELAYED)
        Shipment.objects.create(departureLocation="Krakow", destinationLocation="New York")

    def setUp(self):
        self.factory = RequestFactory()
        self.my_admin = User.objects.create_superuser(
            'paul', 
            'paul@test.com', 
            'lisanalgaib'
        )


    def test_get_all_shipments(self):
        request = self.factory.get('/shipments/')
        force_authenticate(request, user=self.my_admin)
        response = ShipmentViewSet.as_view({'get': 'list'})(request)

        shipments = Shipment.objects.all()
        serializer = ShipmentSerializer(shipments, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_shipment_create(self):
        data = json.dumps({
            "departureLocation": "Berlin",
            "destinationLocation": "Frankfurt"
        })
        client = APIClient()
        client.force_authenticate(user=self.my_admin)
        response = client.post('/shipments/', data=data, content_type='application/json')
        # Check if you get a 200 back:
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check shipment is created
        shipment = Shipment.objects.get(departureLocation="Berlin")
        self.assertEqual(shipment.departureLocation, 'Berlin')