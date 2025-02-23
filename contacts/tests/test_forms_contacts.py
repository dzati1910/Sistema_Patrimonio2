import pytest
from django.core.exceptions import ValidationError
from contacts.forms import SupplierForm

# Test valid form data
@pytest.mark.django_db
def test_supplier_form_valid_data():
    form_data = {
        'name': 'Test Supplier',
        'tax_id': '12345678901234',
        'contact': '98765432109876',
    }
    form = SupplierForm(data=form_data)
    assert form.is_valid()

# Test invalid form data - name field is empty
@pytest.mark.django_db
def test_supplier_form_invalid_name():
    form_data = {
        'name': '',
        'tax_id': '12345678901234',
        'contact': '98765432109876',
    }
    form = SupplierForm(data=form_data)
    assert not form.is_valid()
    assert 'name' in form.errors

# Test invalid form data - tax_id field is empty
@pytest.mark.django_db
def test_supplier_form_invalid_tax_id_digits():
    form_data = {
        'name': 'Test Supplier',
        'tax_id': '1234567890123',  # Only 13 digits
        'contact': '98765432109876',
    }
    form = SupplierForm(data=form_data)
    assert not form.is_valid()
    assert 'tax_id' in form.errors
    assert 'O campo deve conter exatamente 14 dígitos numéricos' in form.errors['tax_id'][0]
# Test invalid form data - contact field is empty
@pytest.mark.django_db
def test_supplier_form_invalid_contact():
    form_data = {
        'name': 'Test Supplier',
        'tax_id': '12345678901234',
        'contact': '',
    }
    form = SupplierForm(data=form_data)
    assert not form.is_valid()
    assert 'contact' in form.errors

# Test invalid form data - contact field does not have 14 digits
@pytest.mark.django_db
def test_supplier_form_invalid_contact_digits():
    form_data = {
        'name': 'Test Supplier',
        'tax_id': '12345678901234',
        'contact': '1234567890123',  # Only 13 digits
    }
    form = SupplierForm(data=form_data)
    assert not form.is_valid()
    assert 'contact' in form.errors

# Test invalid form data - tax_id field does not have 14 digits
@pytest.mark.django_db
def test_supplier_form_invalid_tax_id_digits():
    form_data = {
        'name': 'Test Supplier',
        'tax_id': '1234567890123',  # Only 13 digits
        'contact': '98765432109876',
    }
    form = SupplierForm(data=form_data)
    assert not form.is_valid()
    assert 'tax_id' in form.errors

# Test form save method
@pytest.mark.django_db
def test_supplier_form_save():
    form_data = {
        'name': 'Test Supplier',
        'tax_id': '12345678901234',
        'contact': '98765432109876',
    }
    form = SupplierForm(data=form_data)
    assert form.is_valid()
    supplier = form.save()
    assert supplier.name == 'Test Supplier'
    assert supplier.tax_id == '12345678901234'
    assert supplier.contact == '98765432109876'