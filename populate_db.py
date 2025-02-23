import random
from faker import Faker
from assets.models import Category, Department, Property
from contacts.models import Supplier

fake = Faker()

def create_or_get_category(name):
    category, created = Category.objects.get_or_create(name=name)
    return category

def create_department():
    return Department.objects.create(
        name=fake.company(),
        location=fake.city(),
        responsible_person=None
    )

def create_supplier():
    tax_id = fake.numerify(text="##############")
    while Supplier.objects.filter(tax_id=tax_id).exists():
        tax_id = fake.numerify(text="##############")
    return Supplier.objects.create(
        name=fake.company(),
        tax_id=tax_id,
        contact=fake.numerify(text="##############")
    )

def create_property():
    rfid_tag = fake.hexify(text="^^^^^^^^^^^^", upper=True)  # 12 caracteres hexadecimais
    while Property.objects.filter(rfid_tag=rfid_tag).exists():
        rfid_tag = fake.hexify(text="^^^^^^^^^^^^", upper=True)
    return Property.objects.create(
        name=fake.word().capitalize() + " Asset",
        category=random.choice(Category.objects.all()),
        department=random.choice(Department.objects.all()),
        supplier=random.choice(Supplier.objects.all()),
        rfid_tag=rfid_tag,
        quantity=fake.random_int(min=1, max=100),
        value=fake.random_number(digits=5, fix_len=True)
    )

def run():
    # Cria categorias
    category1 = create_or_get_category("Eletrônicos")
    category2 = create_or_get_category("Móveis")

    # Cria departamentos
    department1 = create_department()
    department2 = create_department()

    # Cria fornecedores
    supplier1 = create_supplier()
    supplier2 = create_supplier()

    # Cria propriedades
    for _ in range(10):
        create_property()

    print("Dados fictícios criados com sucesso!")