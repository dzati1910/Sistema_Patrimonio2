# test_forms.py
import pytest
from django import forms
from django.utils.translation import gettext as _
from assets.models import Category, Department, Property, Supplier, Contract
from assets.forms import (
    ContractForm,
    CategoryForm,
    DepartmentForm,
    AdminPropertyForm,
    PropertyForm
)

# ContractForm Tests
@pytest.mark.django_db
def test_contract_form_meta_configuration():
    assert ContractForm.Meta.model == Contract
    assert ContractForm.Meta.fields == [
        'property', 'supplier', 'start_date', 'end_date', 'value'
    ]


@pytest.mark.django_db
def test_contract_form_widgets():
    form = ContractForm()

    # Verifica se o widget é DateInput
    assert isinstance(form.fields['start_date'].widget, forms.DateInput)
    assert isinstance(form.fields['end_date'].widget, forms.DateInput)

    # Verifica o HTML renderizado para o atributo 'type'
    start_date_html = form['start_date'].as_widget()
    assert 'type="date"' in start_date_html

    end_date_html = form['end_date'].as_widget()
    assert 'type="date"' in end_date_html

# CategoryForm Tests
@pytest.mark.django_db
def test_category_form_meta_configuration():
    assert CategoryForm.Meta.model == Category
    assert CategoryForm.Meta.fields == ['name']

@pytest.mark.django_db
def test_category_form_widget():
    form = CategoryForm()
    assert 'class="form-control"' in str(form['name'])

@pytest.mark.django_db
def test_category_form_validation():
    form = CategoryForm(data={'name': ''})
    assert not form.is_valid()
    assert 'name' in form.errors

# DepartmentForm Tests
@pytest.mark.django_db
def test_department_form_meta_configuration():
    assert DepartmentForm.Meta.model == Department
    assert DepartmentForm.Meta.fields == [
        'name', 'location', 'responsible_person'
    ]

@pytest.mark.django_db
def test_department_form_widgets():
    form = DepartmentForm()
    assert 'class="form-control"' in str(form['name'])
    assert 'class="form-control"' in str(form['location'])
    assert 'class="form-select"' in str(form['responsible_person'])

# AdminPropertyForm Tests
@pytest.mark.django_db
def test_admin_property_form_meta_configuration():
    assert AdminPropertyForm.Meta.model == Property
    assert AdminPropertyForm.Meta.fields == [
        'name', 'category', 'supplier', 'department', 'rfid_tag', 'quantity', 'value'
    ]

@pytest.mark.django_db
def test_admin_property_form_rfid_uniqueness():
    category = Category.objects.create(name='Electronics')
    supplier = Supplier.objects.create(name='Supplier X')
    department = Department.objects.create(name='HR', location='Building B')
    Property.objects.create(
        name='Tablet',
        category=category,
        supplier=supplier,
        department=department,
        rfid_tag='RFID123',
        quantity=10,
        value=200
    )
    form_data = {
        'name': 'Phone',
        'category': category.id,
        'supplier': supplier.id,
        'department': department.id,
        'rfid_tag': 'RFID123',
        'quantity': 5,
        'value': 500
    }
    form = AdminPropertyForm(data=form_data)
    assert not form.is_valid()
    assert 'rfid_tag' in form.errors
    assert 'já está sendo utilizado' in form.errors['rfid_tag'][0]

@pytest.mark.django_db
def test_admin_property_form_update_rfid():
    category = Category.objects.create(name='Electronics')
    supplier = Supplier.objects.create(name='Supplier X')
    department = Department.objects.create(name='HR', location='Building B')
    prop = Property.objects.create(
        name='Tablet',
        category=category,
        supplier=supplier,
        department=department,
        rfid_tag='RFID123',
        quantity=10,
        value=200
    )
    form_data = {
        'name': 'Tablet Updated',
        'category': category.id,
        'supplier': supplier.id,
        'department': department.id,
        'rfid_tag': 'RFID123',  # Same RFID
        'quantity': 15,
        'value': 300
    }
    form = AdminPropertyForm(data=form_data, instance=prop)
    assert form.is_valid()

# PropertyForm Tests
@pytest.mark.django_db
def test_property_form_meta_configuration():
    assert PropertyForm.Meta.model == Property
    assert PropertyForm.Meta.fields == ['quantity', 'value']

@pytest.mark.django_db
def test_property_form_widgets():
    form = PropertyForm()
    assert 'class="form-control"' in str(form['quantity'])

@pytest.mark.django_db
def test_property_form_does_not_include_rfid():
    form = PropertyForm()
    assert 'rfid_tag' not in form.fields