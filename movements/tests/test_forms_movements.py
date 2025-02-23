# movements/tests/test_forms.py
import pytest
from django import forms
from django.core.exceptions import ValidationError
from assets.models import Category, Department, Supplier, Property
from movements.forms import MovementForm


# Fixtures
@pytest.fixture
def category(db):
    return Category.objects.create(name="Eletrônicos")


@pytest.fixture
def supplier(db):
    return Supplier.objects.create(
        name="Fornecedor X",
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
def test_form_widgets_and_classes():
    """Verifica configuração dos widgets e classes CSS"""
    form = MovementForm()

    # Testa widgets
    assert isinstance(form.fields['property'].widget, forms.Select)
    assert isinstance(form.fields['origin_department'].widget, forms.Select)
    assert isinstance(form.fields['destination_department'].widget, forms.Select)

    # Testa classes
    for field in ['property', 'origin_department', 'destination_department']:
        assert 'form-select' in form.fields[field].widget.attrs['class']


@pytest.mark.django_db
def test_valid_form_submission(property_instance, origin_department, destination_department):
    """Teste de submissão válida"""
    form_data = {
        'property': property_instance.id,
        'origin_department': origin_department.id,
        'destination_department': destination_department.id
    }

    form = MovementForm(data=form_data)
    assert form.is_valid(), f"Erros encontrados: {form.errors}"

    movement = form.save()
    assert movement.property == property_instance
    assert movement.origin_department == origin_department
    assert movement.destination_department == destination_department


@pytest.mark.django_db
def test_same_departments_error(property_instance, origin_department):
    """Teste de departamentos iguais"""
    form_data = {
        'property': property_instance.id,
        'origin_department': origin_department.id,
        'destination_department': origin_department.id  # Campo inválido
    }

    form = MovementForm(data=form_data)
    assert not form.is_valid()
    assert 'destination_department' in form.errors
    assert 'devem ser diferentes' in form.errors['destination_department'][0]


@pytest.mark.django_db
def test_origin_department_mismatch_error(property_instance, destination_department):
    """Teste de departamento de origem incorreto"""
    wrong_department = Department.objects.create(name="Financeiro", location="Sala 301")

    form_data = {
        'property': property_instance.id,
        'origin_department': wrong_department.id,
        'destination_department': destination_department.id
    }

    form = MovementForm(data=form_data)
    assert not form.is_valid()
    assert 'origin_department' in form.errors
    assert 'não está localizado' in form.errors['origin_department'][0]


@pytest.mark.django_db
def test_missing_required_fields():
    """Teste de campos obrigatórios faltantes"""
    form_data = {}  # Dados vazios
    form = MovementForm(data=form_data)
    assert not form.is_valid()
    assert 'property' in form.errors
    assert 'origin_department' in form.errors
    assert 'destination_department' in form.errors


@pytest.mark.django_db
def test_auto_department_assignment(property_instance, origin_department, destination_department):
    """Teste de atualização automática do departamento do bem"""
    form_data = {
        'property': property_instance.id,
        'origin_department': origin_department.id,
        'destination_department': destination_department.id
    }

    form = MovementForm(data=form_data)
    assert form.is_valid()

    movement = form.save()
    property_instance.refresh_from_db()
    assert property_instance.department == destination_department