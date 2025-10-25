#!/usr/bin/env python
"""
Script to create test data for the iTalk VoIP system.
Run this after migrations: python manage.py shell < setup_test_data.py
"""
from api.models import Domain, Extension, Customer
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'italkvoip.settings')
django.setup()


# Create test domain
domain, created = Domain.objects.get_or_create(
    name="iTalk Main",
    defaults={'sip_url': 'sip:69.164.245.27'}
)
print(f"Domain {'created' if created else 'already exists'}: {domain}")

# Create test extensions (only if they don't exist)
extensions_data = [
    {"number": "1001", "password": "pass1001"},
    {"number": "1002", "password": "secretpass123"},
    {"number": "1003", "password": "pass1003"},
    {"number": "1004", "password": "pass1004"},
    {"number": "1005", "password": "pass1005"},
]

for ext_data in extensions_data:
    extension, created = Extension.objects.get_or_create(
        number=ext_data["number"],
        defaults={
            'password': ext_data["password"],
            'domain': domain,
            'enabled': True
        }
    )
    print(
        f"Extension {ext_data['number']} {'created' if created else 'already exists'}")

print(f"\nTotal extensions available: {Extension.objects.count()}")
print(f"Total customers: {Customer.objects.count()}")
print("\nSetup complete! You can now test the API.")
