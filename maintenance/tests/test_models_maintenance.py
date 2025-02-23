# maintenance/tests/test_models_maintenance.py
from datetime import date

import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone
from assets.models import Property, Category, Department
from contacts.models import Supplier
from maintenance.models import Maintenance


# Fixtures para modelos relacionados
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
        scheduled_date=timezone.now().date() + timezone.timedelta(days=7),
        cost=500.00,
        description='Manutenção preventiva'
    )


# Testes do modelo Maintenance
@pytest.mark.django_db
def test_maintenance_creation(property_instance):
    """Teste corrigido com manipulação correta de datas"""
    # Criar usando objeto date
    test_date = date(2024, 1, 15)

    maintenance = Maintenance.objects.create(
        property=property_instance,
        scheduled_date=test_date,
        cost=1000.00,
        description='Manutenção inicial'
    )

    # Verificar tipos e valores
    assert isinstance(maintenance.scheduled_date, date)
    assert maintenance.scheduled_date == test_date
    assert str(maintenance.scheduled_date) == '2024-01-15'  # Opcional: verificar formatação


@pytest.mark.django_db
def test_optional_fields(property_instance):
    """Teste corrigido para datas e campos opcionais"""
    maintenance = Maintenance.objects.create(
        property=property_instance,
        scheduled_date=date(2024, 1, 15),
        cost=750.50,
        completion_date=date(2024, 1, 16),  # Usar objeto date
        description='Troca de componentes'
    )

    assert maintenance.completion_date == date(2024, 1, 16)
    assert isinstance(maintenance.completion_date, date)


def test_status_choices(property_instance):
    valid_statuses = ['Agendado', 'Em Manutenção', 'Completado']

    for status in valid_statuses:
        maintenance = Maintenance(
            property=property_instance,
            scheduled_date='2024-01-15',
            cost=300.00,
            status=status,
            description='Descrição padrão'  # Adicionado
        )
        maintenance.full_clean()


@pytest.mark.django_db
def test_default_status(property_instance):
    """Verifica o valor padrão do campo status"""
    maintenance = Maintenance.objects.create(
        property=property_instance,
        scheduled_date='2024-01-15',
        cost=200.00
    )
    assert maintenance.status == 'Agendado'


@pytest.mark.django_db
def test_is_overdue_method(property_instance):
    """Testa a lógica de manutenção atrasada em diferentes cenários"""
    today = timezone.now().date()

    # Caso 1: Manutenção atrasada
    overdue = Maintenance.objects.create(
        property=property_instance,
        scheduled_date=today - timezone.timedelta(days=5),
        cost=300.00
    )
    assert overdue.is_overdue() is True

    # Caso 2: Manutenção concluída
    completed = Maintenance.objects.create(
        property=property_instance,
        scheduled_date=today - timezone.timedelta(days=3),
        completion_date=today - timezone.timedelta(days=1),
        cost=400.00,
        status='Completado'
    )
    assert completed.is_overdue() is False

    # Caso 3: Manutenção futura
    future = Maintenance.objects.create(
        property=property_instance,
        scheduled_date=today + timezone.timedelta(days=10),
        cost=500.00
    )
    assert future.is_overdue() is False


@pytest.mark.django_db
def test_cost_validation(property_instance):
    """Teste corrigido para mensagem de erro e campos obrigatórios"""
    with pytest.raises(ValidationError) as error:
        Maintenance(
            property=property_instance,
            scheduled_date=date(2024, 1, 15),
            cost=12345.678,  # Valor inválido com 3 casas decimais
            description='Descrição obrigatória'  # Campo necessário
        ).full_clean()

    # Verificar mensagem exata do Django
    assert 'Certifique-se de que não tenha mais de 2 casas decimais.' in str(error.value)


@pytest.mark.django_db
def test_dates_validation(property_instance):
    """Valida a relação entre datas de agendamento e conclusão"""
    with pytest.raises(ValidationError):
        invalid = Maintenance(
            property=property_instance,
            scheduled_date='2024-01-15',
            completion_date='2024-01-10',
            cost=500.00
        )
        invalid.full_clean()