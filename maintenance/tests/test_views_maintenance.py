# maintenance/tests/test_views_maintenance.py
import pytest
from datetime import date, timedelta
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from assets.models import Property, Category, Department
from contacts.models import Supplier
from maintenance.forms import MaintenanceForm
from maintenance.models import Maintenance

User = get_user_model()


# Fixtures
@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='testpass')


@pytest.fixture
def category(db):
    return Category.objects.create(name='Eletrônicos')


@pytest.fixture
def department(db):
    return Department.objects.create(name='TI', location='Sala 101')


@pytest.fixture
def supplier(db):
    return Supplier.objects.create(
        name='Fornecedor Principal',
        tax_id='12345678901234',
        contact='55119999999999'
    )


@pytest.fixture
def property_instance(db, category, department, supplier):
    return Property.objects.create(
        name='Notebook Dell',
        category=category,
        department=department,
        supplier=supplier,
        rfid_tag='RFID123456',
        quantity=5,
        value=15000.00
    )


@pytest.fixture
def maintenance_instance(db, property_instance):
    return Maintenance.objects.create(
        property=property_instance,
        scheduled_date=date.today() + timedelta(days=7),
        cost=500.00,
        description='Manutenção preventiva',
        status='Agendado'
    )


# Testes para MaintenanceListView
@pytest.mark.django_db
def test_maintenance_list_unauthenticated(client):
    response = client.get(reverse('list-maintenance'))
    assert response.status_code == 302
    assert '/core/login/' in response.url


@pytest.mark.django_db
def test_maintenance_list_authenticated(client, user, maintenance_instance):
    client.force_login(user)
    response = client.get(reverse('list-maintenance'))
    assert response.status_code == 200
    assert 'list-maintenance.html' in [t.name for t in response.templates]
    assert maintenance_instance in response.context['maintenance']


# Testes para MaintenanceCreateView
@pytest.mark.django_db
def test_maintenance_create_get(client, user):
    client.force_login(user)
    response = client.get(reverse('create-maintenance'))
    assert response.status_code == 200
    assert 'modals/create_maintenance.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_maintenance_create_post_valid(client, user, property_instance):
    client.force_login(user)
    data = {
        'property': property_instance.id,
        'scheduled_date': date.today() + timedelta(days=5),
        'cost': 750.50,
        'description': 'Nova manutenção',
        'status': 'Agendado'
    }
    response = client.post(reverse('create-maintenance'), data)
    assert response.status_code == 302
    assert Maintenance.objects.filter(description='Nova manutenção').exists()


# Testes para MaintenanceUpdateView
def test_form_update_disabled_fields(maintenance_instance):
    form = MaintenanceForm(instance=maintenance_instance)

    # Verificar campos que não devem existir
    assert 'property' not in form.fields
    assert 'scheduled_date' not in form.fields

    # Verificar campos que existem
    assert form.fields['completion_date'].disabled is False
    assert form.fields['cost'].disabled is False


# Testes para MaintenanceDeleteView
@pytest.mark.django_db
def test_maintenance_delete_get(client, user, maintenance_instance):
    client.force_login(user)
    response = client.get(reverse('maintenance-confirm-delete', kwargs={'pk': maintenance_instance.pk}))
    assert response.status_code == 200
    assert 'modals/maintenance-confirm-delete.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_maintenance_delete_post(client, user, maintenance_instance):
    client.force_login(user)
    response = client.post(reverse('maintenance-confirm-delete', kwargs={'pk': maintenance_instance.pk}))
    assert response.status_code == 302
    assert not Maintenance.objects.filter(pk=maintenance_instance.pk).exists()


