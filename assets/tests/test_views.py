# test_views.py
import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.template.loader import get_template
from assets.models import Contract, Category, Department, Property, Supplier

User = get_user_model()  # Usar o modelo customizado

# Fixtures
@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='testpass')

@pytest.fixture
def category(db):
    return Category.objects.create(name='Electronics')

@pytest.fixture
def supplier(db):
    return Supplier.objects.create(name='Tech Supplier')

@pytest.fixture
def department(db):
    return Department.objects.create(name='IT', location='Building A')

@pytest.fixture
def property_instance(db, category, supplier, department):
    return Property.objects.create(
        name='Laptop',
        category=category,
        supplier=supplier,
        department=department,
        rfid_tag='RFID123',
        quantity=5,
        value=1500
    )

@pytest.fixture
def contract(db, property_instance, supplier):
    return Contract.objects.create(
        property=property_instance,
        supplier=supplier,
        start_date='2024-01-01',  # Campo obrigatório
        end_date='2024-12-31',    # Campo obrigatório
        value=5000
    )

# Testes de autenticação
@pytest.mark.django_db
def test_list_contracts_unauthenticated(client):
    url = reverse('list-contracts')
    response = client.get(url)
    assert response.status_code == 302
    assert '/core/login/' in response.url  # Atualizado para seu caminho de login

@pytest.mark.django_db
def test_index_view_unauthenticated(client):
    response = client.get(reverse('list-property'))
    assert response.status_code == 302
    assert '/core/login/' in response.url

# Testes de views autenticadas
@pytest.mark.django_db
def test_list_contracts_authenticated(client, user):
    client.force_login(user)
    response = client.get(reverse('list-contracts'))
    assert response.status_code == 200
    assert 'list-contracts.html' in [t.name for t in response.templates]

@pytest.mark.django_db
def test_contract_create_view_get(client, user):
    client.force_login(user)
    response = client.get(reverse('create-contracts'))
    assert response.status_code == 200
    assert 'modals/create_contracts.html' in [t.name for t in response.templates]

@pytest.mark.django_db
def test_contract_create_view_post(client, user, property_instance, supplier):
    client.force_login(user)
    data = {
        'property': property_instance.id,
        'supplier': supplier.id,
        'start_date': '2024-01-01',
        'end_date': '2025-01-01',
        'value': 10000
    }
    response = client.post(reverse('create-contracts'), data)
    assert response.status_code == 302
    assert Contract.objects.filter(value=10000).exists()

# Testes de Categorias
@pytest.mark.django_db
def test_category_delete_view_post(client, user, category):
    client.force_login(user)
    url = reverse('category-confirm-delete', kwargs={'pk': category.pk})
    response = client.post(url)
    assert response.status_code == 302
    assert not Category.objects.filter(pk=category.pk).exists()

# Testes de Departamentos
@pytest.mark.django_db
def test_department_create_view_post(client, user):
    client.force_login(user)
    data = {'name': 'HR', 'location': 'Building B'}
    response = client.post(reverse('create-department'), data)
    assert response.status_code == 302
    assert Department.objects.filter(name='HR').exists()

# Testes de Propriedades
@pytest.mark.django_db
def test_property_create_view_post(client, user, category, supplier, department):
    client.force_login(user)
    data = {
        'name': 'Tablet',
        'category': category.id,
        'supplier': supplier.id,
        'department': department.id,
        'rfid_tag': 'RFID456',
        'quantity': 10,
        'value': 2000
    }
    response = client.post(reverse('create-property'), data)
    assert response.status_code == 302
    assert Property.objects.filter(rfid_tag='RFID456').exists()

@pytest.mark.django_db
def test_property_update_view_get(client, user, property_instance):
    client.force_login(user)
    url = reverse('update-property', kwargs={'pk': property_instance.pk})
    response = client.get(url)
    assert response.status_code == 200
    assert 'modals/update_property.html' in [t.name for t in response.templates]

# Teste de view Index
@pytest.mark.django_db
def test_index_view_authenticated(client, user):
    client.force_login(user)
    response = client.get(reverse('list-property'))
    assert response.status_code == 200
    assert response.templates[0].name == 'list-property.html'
    assert 'properties' in response.context

# Testes de métodos HTTP inválidos
@pytest.mark.django_db
def test_contract_delete_view_invalid_method(client, user, contract):
    client.force_login(user)
    url = reverse('contract-confirm-delete', kwargs={'pk': contract.pk})

    # Testar método PUT não permitido
    response = client.put(url)
    assert response.status_code == 405

    # Verificar que o contrato ainda existe
    assert Contract.objects.filter(pk=contract.pk).exists()

# Teste de template customizado
@pytest.mark.django_db
def test_custom_login_template(client):
    response = client.get('/core/login/')
    assert response.status_code == 200
    assert 'modals/login.html' in [t.name for t in response.templates]