import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils import timezone
from contacts.models import Supplier
from assets.models import Contract, Property  # Import the Property model

# Fixtures for test data
@pytest.fixture
def supplier(db):
    return Supplier.objects.create(
        name="Test Supplier",
        tax_id="12345678901234",
        contact="98765432109876",
    )

@pytest.fixture
def another_supplier(db):
    return Supplier.objects.create(
        name="Another Supplier",
        tax_id="98765432109876",
        contact="12345678901234",
    )

@pytest.fixture
def property(db):  # Create a fixture for the Property model
    return Property.objects.create(
        name="Test Property",
    )

# Test field validations
@pytest.mark.django_db
def test_supplier_contact_validator():
    with pytest.raises(ValidationError):
        supplier = Supplier(
            name="Invalid Supplier",
            tax_id="12345678901234",
            contact="invalid_contact",
        )
        supplier.full_clean()  # Manually trigger validation
        supplier.save()

@pytest.mark.django_db
def test_supplier_tax_id_unique_constraint():
    Supplier.objects.create(
        name="First Supplier",
        tax_id="12345678901234",
        contact="98765432109876",
    )
    with pytest.raises(IntegrityError):
        Supplier.objects.create(
            name="Second Supplier",
            tax_id="12345678901234",
            contact="12345678901234",
        )

@pytest.mark.django_db
def test_supplier_contact_unique_constraint():
    Supplier.objects.create(
        name="First Supplier",
        tax_id="12345678901234",
        contact="98765432109876",
    )
    with pytest.raises(IntegrityError):
        Supplier.objects.create(
            name="Second Supplier",
            tax_id="98765432109876",
            contact="98765432109876",
        )

@pytest.mark.django_db
def test_supplier_str_representation(supplier):
    assert str(supplier) == "Test Supplier"