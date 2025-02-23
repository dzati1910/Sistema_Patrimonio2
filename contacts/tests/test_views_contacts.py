# test_views.py
import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from contacts.models import Supplier
from rest_framework.test import APIClient
User = get_user_model()

# Fixtures
@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='testpass')

@pytest.fixture
def supplier(db):
    return Supplier.objects.create(
        name='Fornecedor Teste',
        tax_id='12345678901234',
        contact='55119999999999'
    )

# Testes para list_contacts
@pytest.mark.django_db
def test_list_contacts_unauthenticated(client):
    response = client.get(reverse('list-contacts'))
    assert response.status_code == 302
    assert '/core/login/' in response.url

@pytest.mark.django_db
def test_list_contacts_authenticated(client, user, supplier):
    client.force_login(user)
    response = client.get(reverse('list-contacts'))
    assert response.status_code == 200
    assert 'list-contacts.html' in [t.name for t in response.templates]
    assert supplier in response.context['contacts']

# Testes para SupplierCreateView
@pytest.mark.django_db
def test_supplier_create_view_get(client, user):
    client.force_login(user)
    response = client.get(reverse('create-contacts'))
    assert response.status_code == 200
    assert 'modals/create_supplier.html' in [t.name for t in response.templates]

@pytest.mark.django_db
def test_supplier_create_view_post_valid(client, user):
    client.force_login(user)
    data = {
        'name': 'Novo Fornecedor',
        'tax_id': '11223344556677',
        'contact': '55118888888888'
    }
    response = client.post(reverse('create-contacts'), data)
    assert response.status_code == 302
    assert Supplier.objects.filter(name='Novo Fornecedor').exists()

@pytest.mark.django_db
def test_supplier_create_view_post_invalid(client, user):
    client.force_login(user)
    data = {
        'name': 'Fornecedor Inválido',
        'tax_id': '123',  # Formato inválido
        'contact': '1199999'  # Formato inválido
    }
    response = client.post(reverse('create-contacts'), data)
    assert response.status_code == 200
    assert 'form' in response.context
    assert response.context['form'].errors

# Testes para SupplierUpdateView
@pytest.mark.django_db
def test_supplier_update_view_get(client, user, supplier):
    client.force_login(user)
    response = client.get(reverse('update-contacts', kwargs={'pk': supplier.pk}))
    assert response.status_code == 200
    assert 'modals/create_supplier.html' in [t.name for t in response.templates]

@pytest.mark.django_db
def test_supplier_update_view_post(client, user, supplier):
    client.force_login(user)
    data = {
        'name': 'Fornecedor Atualizado',
        'tax_id': supplier.tax_id,  # Mantém o mesmo CNPJ
        'contact': supplier.contact  # Mantém o mesmo contato
    }
    response = client.post(reverse('update-contacts', kwargs={'pk': supplier.pk}), data)
    assert response.status_code == 302
    supplier.refresh_from_db()
    assert supplier.name == 'Fornecedor Atualizado'

# Testes para SupplierDeleteView
@pytest.mark.django_db
def test_supplier_delete_view_get(client, user, supplier):
    client.force_login(user)
    response = client.get(reverse('supplier-confirm-delete', kwargs={'pk': supplier.pk}))
    assert response.status_code == 200
    assert 'modals/supplier-confirm-delete.html' in [t.name for t in response.templates]

@pytest.mark.django_db
def test_supplier_delete_view_post(client, user, supplier):
    client.force_login(user)
    response = client.post(reverse('supplier-confirm-delete', kwargs={'pk': supplier.pk}))
    assert response.status_code == 302
    assert not Supplier.objects.filter(pk=supplier.pk).exists()


# Teste para a propriedade active_contracts
@pytest.mark.django_db
def test_supplier_active_contracts(supplier):
    # Cria contratos associados (dependendo da model Contract)
    # Exemplo hipotético:
    # Contract.objects.create(supplier=supplier, start_date=..., end_date=...)
    assert supplier.active_contracts == 0  # Ajustar conforme implementação real