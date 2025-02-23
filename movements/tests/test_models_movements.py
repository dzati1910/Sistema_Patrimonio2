import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone
from assets.models import Category, Department, Supplier, Property
from movements.models import Movement

# Fixtures
@pytest.fixture
def category(db):
    return Category.objects.create(name="Eletrônicos")


@pytest.fixture
def supplier(db):
    return Supplier.objects.create(
        name="Fornecedor A",
        tax_id="12345678901234",
        contact="55119999999999"
    )


@pytest.fixture
def origin_department(db):
    return Department.objects.create(name="TI", location="Sala 101")


@pytest.fixture
def destination_department(db):
    return Department.objects.create(name="RH", location="Sala 201")


@pytest.fixture
def property_instance(db, category, origin_department, supplier):
    return Property.objects.create(
        name="Notebook Dell",
        category=category,
        department=origin_department,
        supplier=supplier,
        rfid_tag="RFID123",
        quantity=5,
        value=15000.00
    )


# Testes
@pytest.mark.django_db
def test_valid_movement_creation(property_instance, origin_department, destination_department):
    movement = Movement.objects.create(
        property=property_instance,
        origin_department=origin_department,
        destination_department=destination_department
    )

    assert movement.property == property_instance
    assert movement.origin_department == origin_department
    assert movement.destination_department == destination_department
    assert movement.timestamp is not None



@pytest.mark.django_db
def test_auto_timestamp(property_instance, origin_department, destination_department):
    movement = Movement.objects.create(
        property=property_instance,
        origin_department=origin_department,
        destination_department=destination_department
    )

    assert movement.timestamp is not None
    assert movement.timestamp.date() == timezone.now().date()  # Corrigido com a importação