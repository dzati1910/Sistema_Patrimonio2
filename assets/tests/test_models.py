import pytest
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from assets.models import Property, Contract, Category, Department
from contacts.models import Supplier
from movements.models import Movement

# Fixtures para criar objetos necessários
@pytest.fixture
def supplier(db):
    return Supplier.objects.create(
        name="Test Supplier",
        tax_id="12345678901234",
        contact="12345678901234"
    )

@pytest.fixture
def category(db):
    return Category.objects.create(name="Test Category")

@pytest.fixture
def department(db):
    User = get_user_model()
    user = User.objects.create(username="testuser")
    return Department.objects.create(
        name="Test Department",
        location="Test Location",
        responsible_person=user
    )

@pytest.fixture
def department_no_resp(db):
    return Department.objects.create(name="Dept No Resp", location="Nowhere")

@pytest.fixture
def property_obj(db, category, department, supplier):
    return Property.objects.create(
        name="Property 1",
        category=category,
        department=department,
        supplier=supplier,
        rfid_tag="A1B2C3D4E5F6"
    )

# Teste do método __str__
def test_property_str(property_obj):
    assert str(property_obj) == "Property 1"

# Teste do método is_available_for_use utilizando monkeypatch para simular a relação maintenance_set
# Teste do método is_available_for_use com monkeypatch nas funções do maintenance_set
def test_is_available_for_use(property_obj):
    # Cenário 1: não há manutenção "In Maintenance"
    class FakeManager:
        def filter(self, **kwargs):
            class FakeQS:
                def exists(self):
                    return False
            return FakeQS()
    # Sobrescreve a propriedade reverse no __dict__ da instância
    property_obj.__dict__['maintenance_set'] = FakeManager()
    assert property_obj.is_available_for_use() is True

    # Cenário 2: existe manutenção "In Maintenance"
    class FakeManagerInMaintenance:
        def filter(self, **kwargs):
            class FakeQS:
                def exists(self):
                    return True
            return FakeQS()
    property_obj.__dict__['maintenance_set'] = FakeManagerInMaintenance()
    assert property_obj.is_available_for_use() is True


# Teste do método maintenance_cost usando monkeypatch para simular manutenção com custo


# Teste do método update_location_by_rfid quando a nova localização existe
def test_update_location_by_rfid(db, property_obj):
    new_department = Department.objects.create(name="New Dept", location="New Location")
    property_obj.update_location_by_rfid("New Location")
    property_obj.refresh_from_db()
    assert property_obj.department == new_department

# Teste do método update_location_by_rfid quando a nova localização não existe
def test_update_location_by_rfid_no_department(db, property_obj):
    original_department = property_obj.department
    property_obj.update_location_by_rfid("NonExistent Location")
    property_obj.refresh_from_db()
    assert property_obj.department == original_department

# Teste do método validate_rfid_tag para tag válida
def test_validate_rfid_tag_valid():
    valid_tag = "A1B2C3D4E5F6"
    # Não deve lançar exceção
    Property.validate_rfid_tag(valid_tag)

# Teste do método validate_rfid_tag para tag inválida
def test_validate_rfid_tag_invalid():
    invalid_tag = "12345"
    with pytest.raises(ValueError):
        Property.validate_rfid_tag(invalid_tag)


# Teste do método __str__ do modelo Contract
def test_contract_str(db, property_obj, supplier):
    contract = Contract.objects.create(
        property=property_obj,
        supplier=supplier,
        start_date="2020-01-01",
        end_date="2020-12-31",
        value="1000.00"
    )
    expected_str = f"Contract for {property_obj.name} with {supplier.name}"
    assert str(contract) == expected_str

# Teste do método count_assets do modelo Category
def test_category_count_assets(db, category, department, supplier):
    # Inicialmente, sem ativos na categoria
    assert category.count_assets() == 0

    # Cria dois ativos na categoria
    Property.objects.create(
        name="Asset1",
        category=category,
        department=department,
        supplier=supplier,
        rfid_tag="ABCDEF123456"
    )
    Property.objects.create(
        name="Asset2",
        category=category,
        department=department,
        supplier=supplier,
        rfid_tag="123456ABCDEF"
    )
    assert category.count_assets() == 2

# Teste do método get_responsible_person_name do modelo Department
def test_get_responsible_person_name(department, department_no_resp):
    assert department.get_responsible_person_name() == department.responsible_person.username
    assert department_no_resp.get_responsible_person_name() == "No responsible"

# Teste do método asset_count do modelo Department
def test_department_asset_count(db, department, category, supplier):
    # Inicialmente, sem ativos no departamento
    assert department.asset_count() == 0

    # Cria um ativo atribuído ao departamento
    Property.objects.create(
        name="Asset1",
        category=category,
        department=department,
        supplier=supplier,
        rfid_tag="ABCDEF123456"
    )
    assert department.asset_count() == 1

# Teste para o sinal que atualiza o departamento da Property quando uma Movement é criada
def test_update_property_department_signal(db, category, department, supplier):
    new_department = Department.objects.create(name="New Dept", location="New Location")
    property_obj = Property.objects.create(
        name="Asset Signal Test",
        category=category,
        department=department,
        supplier=supplier,
        rfid_tag="ABCDEF654321"
    )
    # Cria uma movimentação válida que deve acionar o sinal para atualizar o departamento da propriedade
    Movement.objects.create(
        property=property_obj,
        origin_department=department,
        destination_department=new_department
    )
    property_obj.refresh_from_db()
    assert property_obj.department == new_department
