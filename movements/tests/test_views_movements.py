import pytest

from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from assets.models import Category, Department, Supplier, Property
from movements.models import Movement
from movements.forms import MovementForm

User = get_user_model()


# Fixtures
@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='testpass')


@pytest.fixture
def category(db):
    return Category.objects.create(name='Eletrônicos')


@pytest.fixture
def supplier(db):
    return Supplier.objects.create(
        name='Fornecedor X',
        tax_id='12345678901234',
        contact='55119999999999'
    )


@pytest.fixture
def origin_department(db):
    return Department.objects.create(name='TI', location='Sala 101')


@pytest.fixture
def destination_department(db):
    return Department.objects.create(name='RH', location='Sala 201')


@pytest.fixture
def property_instance(db, category, origin_department, supplier):
    return Property.objects.create(
        name='Notebook Dell',
        category=category,
        department=origin_department,
        supplier=supplier,
        rfid_tag='RFID123',
        quantity=5,
        value=15000.00
    )


@pytest.fixture
def movement_instance(db, property_instance, origin_department, destination_department):
    return Movement.objects.create(
        property=property_instance,
        origin_department=origin_department,
        destination_department=destination_department
    )


# Testes para views web
@pytest.mark.django_db
def test_list_movement_unauthenticated(client):
    response = client.get(reverse('list-movement'))
    assert response.status_code == 302
    assert 'core/login/' in response.url


@pytest.mark.django_db
def test_list_movement_authenticated(client, user, movement_instance):
    client.force_login(user)
    response = client.get(reverse('list-movement'))
    assert response.status_code == 200
    assert 'list-movement.html' in [t.name for t in response.templates]
    assert movement_instance in response.context['movements']


@pytest.mark.django_db
def test_movement_create_view_get(client, user):
    client.force_login(user)
    response = client.get(reverse('create-movement'))
    assert response.status_code == 200
    assert 'modals/create_movement.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_movement_create_valid(client, user, property_instance, origin_department, destination_department):
    client.force_login(user)
    data = {
        'property': property_instance.id,
        'origin_department': origin_department.id,
        'destination_department': destination_department.id
    }
    response = client.post(reverse('create-movement'), data)
    assert response.status_code == 302
    assert Movement.objects.filter(property=property_instance).exists()


# movements/tests/test_views_movements.py

@pytest.mark.django_db
def test_movement_delete_view(client, user, movement_instance):
    client.force_login(user)
    response = client.post(reverse('movement-confirm-delete', kwargs={'pk': movement_instance.pk}))
    assert response.status_code == 302
    assert not Movement.objects.filter(pk=movement_instance.pk).exists()


@pytest.mark.django_db
def test_movement_auto_department_update(client, user, property_instance, origin_department, destination_department):
    client.force_login(user)
    data = {
        'property': property_instance.id,
        'origin_department': origin_department.id,
        'destination_department': destination_department.id
    }

    client.post(reverse('create-movement'), data)
    property_instance.refresh_from_db()
    assert property_instance.department == destination_department