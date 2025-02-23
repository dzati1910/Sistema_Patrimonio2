# maintenance/tests/test_forms_maintenance.py
import pytest
from datetime import date, timedelta
from django import forms
from django.core.exceptions import ValidationError
from assets.models import Property, Category, Department
from contacts.models import Supplier
from maintenance.forms import *
from maintenance.models import Maintenance


# Fixtures completas
@pytest.fixture
def category(db):
    return Category.objects.create(name="Eletrônicos")


@pytest.fixture
def department(db):
    return Department.objects.create(name="TI", location="Sala 101")


@pytest.fixture
def supplier(db):
    return Supplier.objects.create(
        name="Fornecedor Principal",
        tax_id="12345678901234",
        contact="55119999999999"
    )


@pytest.fixture
def property_instance(db, category, department, supplier):
    return Property.objects.create(
        name="Notebook Dell",
        category=category,
        department=department,
        supplier=supplier,
        rfid_tag="RFID123456",
        quantity=5,
        value=15000.00
    )


@pytest.fixture
def maintenance_instance(db, property_instance):
    return Maintenance.objects.create(
        property=property_instance,
        scheduled_date=date.today() + timedelta(days=7),
        cost=500.00,
        description="Manutenção preventiva",
        status="Agendado"
    )


def test_form_field_classes():
    form = MaintenanceForm()
    for field_name, field in form.fields.items():
        assert field.widget.attrs.get('class') == 'form-control'


def test_form_update_disabled_fields(maintenance_instance):
    form = MaintenanceForm(instance=maintenance_instance)

    # Campos que realmente existem no MaintenanceForm
    assert 'property' not in form.fields  # Verifica que o campo não existe
    assert 'scheduled_date' not in form.fields
    assert form.fields['completion_date'].disabled is False
    assert form.fields['cost'].disabled is False


@pytest.mark.django_db
def test_completed_status_validation(property_instance):
    form_data = {
        'property': property_instance.id,
        'scheduled_date': date.today(),
        'status': 'Completado',
        'cost': 500.00,
        'description': 'Manutenção sem data de conclusão'
    }

    form = MaintenanceForm(data=form_data)
    assert not form.is_valid()
    assert 'completion_date' in form.errors
    assert 'obrigatória para manutenções completadas' in form.errors['completion_date'][0]


@pytest.mark.django_db
def test_valid_form_submission(property_instance):
    # Usar AdminMaintenanceForm para criação
    form_data = {
        'property': property_instance.id,
        'scheduled_date': date.today() + timedelta(days=5),
        'completion_date': date.today() + timedelta(days=6),
        'status': 'Completado',
        'cost': 750.50,
        'description': 'Manutenção completa'
    }

    form = AdminMaintenanceForm(data=form_data)  # Alterado para AdminMaintenanceForm
    assert form.is_valid()

    maintenance = form.save()
    assert maintenance.status == 'Completado'

def test_date_validation(maintenance_instance):
    invalid_data = {
        'completion_date': maintenance_instance.scheduled_date - timedelta(days=1),
        'cost': 200.00,
        'description': 'Datas inválidas',
        'status': 'Completado'
    }

    form = MaintenanceForm(data=invalid_data, instance=maintenance_instance)
    assert not form.is_valid()
    assert 'completion_date' in form.errors
    assert 'não pode ser anterior' in form.errors['completion_date'][0]