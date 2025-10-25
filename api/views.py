from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.db import transaction
from django.db.models import Exists, OuterRef

from .models import Customer, Extension, Domain
from .serializers import EmailSerializer


class GetCredentialsAPIView(APIView):
    """DRF API view that creates or returns VoIP credentials for a given customer email.

    Accepts POST {"email": "user@example.com"}

    If email exists: returns existing credentials
    If email doesn't exist: creates new customer with available extension

    Returns 200 with {
        "username": "1002", 
        "password": "secretpass123",
        "domain": "69.164.245.27",
        "display_name": "User Name"
    }
    """

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = EmailSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']

        # Try to get existing customer first
        try:
            customer = Customer.objects.select_related(
                'extension__domain').get(email=email)

            # Check if extension is enabled
            if not customer.extension.enabled:
                return Response({'detail': 'Extension is disabled'}, status=status.HTTP_403_FORBIDDEN)

        except Customer.DoesNotExist:
            # Create new customer with available extension
            customer = self._create_customer_with_extension(email)
            if not customer:
                return Response(
                    {'detail': 'No available extensions found'},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE
                )

        ext = customer.extension
        display_name = customer.display_name or email.split(
            '@')[0].capitalize()

        # Remove protocol from sip_url if present
        domain = ext.domain.sip_url.replace(
            'http://', '').replace('https://', '')

        data = {
            'username': ext.number,
            'password': ext.password,
            'domain': domain,
            'display_name': display_name,
        }

        return Response(data, status=status.HTTP_200_OK)

    def _create_customer_with_extension(self, email):
        """Create a new customer and assign an available extension."""
        with transaction.atomic():
            # Find an extension that is not already associated with a customer
            available_extension = Extension.objects.filter(
                enabled=True
            ).exclude(
                Exists(Customer.objects.filter(extension=OuterRef('pk')))
            ).select_related('domain').first()

            if not available_extension:
                return None

            # Create the customer with the available extension
            customer = Customer.objects.create(
                email=email,
                extension=available_extension,
                display_name=email.split('@')[0].capitalize()
            )

            return customer
