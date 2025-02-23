from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from contacts.models import Supplier
from movements.models import Movement


# Modelos do app assets

class Property(models.Model):
    """
    Modelo que representa uma propriedade ou ativo no sistema.
    Contém informações como nome, categoria, departamento, fornecedor, tag RFID, quantidade, valor e datas de criação/atualização.
    """

    name = models.CharField(max_length=200, verbose_name="Name")
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        verbose_name="Category"
    )
    department = models.ForeignKey(
        'Department',
        on_delete=models.CASCADE,
        verbose_name="Department"
    )
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        verbose_name="Supplier"
    )
    rfid_tag = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="RFID Tag"
    )
    quantity = models.IntegerField(default=10)
    value = models.DecimalField(max_digits=10, decimal_places=2, default=10000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Retorna o nome da propriedade."""
        return self.name

    def is_available_for_use(self):
        """
        Verifica se a propriedade está disponível para uso.
        Retorna False se houver manutenções em andamento.
        """
        return not self.maintenance_set.filter(status='In Maintenance').exists()

    def update_location_by_rfid(self, new_location):
        """
        Atualiza o departamento da propriedade com base em uma nova localização.
        """
        try:
            new_department = Department.objects.get(location=new_location)
            self.department = new_department
            self.save()
        except Department.DoesNotExist:
            pass  # Ignora se o departamento não existir

    @staticmethod
    def validate_rfid_tag(rfid_tag):
        """
        Valida o formato da tag RFID (12 dígitos hexadecimais).
        Levanta ValueError se o formato for inválido.
        """
        import re
        pattern = r"^[0-9A-Fa-f]{12}$"
        if not re.match(pattern, rfid_tag):
            raise ValueError("Invalid RFID tag format")

    def maintenance_cost(self):
        """
        Calcula o custo total de manutenção da propriedade.
        Retorna a soma dos custos de todas as manutenções associadas.
        """
        return sum(maintenance.cost for maintenance in self.maintenance_set.all())

    @receiver(post_save, sender=Movement)
    def update_property_department(sender, instance, created, **kwargs):
        """
        Atualiza o departamento da Property para o departamento de destino quando um movimento é salvo.
        A atualização ocorre apenas se o departamento de destino for diferente do atual.
        """
        if instance.property.department_id != instance.destination_department_id:
            # Atualiza apenas o campo 'department' para evitar gatilhos desnecessários
            instance.property.department = instance.destination_department
            instance.property.save(update_fields=['department'])

    class Meta:
        """Metadados do modelo Property."""
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'
        ordering = ['-created_at']


class Contract(models.Model):
    """
    Modelo que representa um contrato associado a uma propriedade e um fornecedor.
    Contém informações sobre datas de início, término e valor do contrato.
    """

    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        """Retorna uma representação legível do contrato."""
        return f"Contract for {self.property.name} with {self.supplier.name}"


class Category(models.Model):
    """
    Modelo que representa uma categoria de propriedades.
    """

    name = models.CharField(max_length=100)

    def count_assets(self):
        """Retorna o número de propriedades associadas a esta categoria."""
        return self.property_set.count()

    def __str__(self):
        """Retorna o nome da categoria."""
        return self.name


class Department(models.Model):
    """
    Modelo que representa um departamento dentro da organização.
    Contém informações sobre nome, localização e pessoa responsável.
    """

    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    responsible_person = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Responsible person"
    )

    def get_responsible_person_name(self):
        """
        Retorna o nome do responsável pelo departamento.
        Se não houver responsável, retorna 'No responsible'.
        """
        return self.responsible_person.username if self.responsible_person else 'No responsible'

    def __str__(self):
        """Retorna o nome do departamento."""
        return self.name

    def asset_count(self):
        """Retorna o número de propriedades associadas ao departamento."""
        return Property.objects.filter(department=self).count()

    class Meta:
        """Metadados do modelo Department."""
        ordering = ['name']
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'