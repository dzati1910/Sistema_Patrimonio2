from django.db import transaction
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from movements.models import Movement
from .models import Property

@receiver(post_save, sender=Movement)
@transaction.atomic
def update_property_department(sender, instance, created, **kwargs):
    """
    Atualiza o departamento da Property para o departamento de destino apenas quando necessário.
    """
    if instance.property.department_id != instance.destination_department_id:
        # Atualize apenas o campo 'department' para evitar gatilhos desnecessários
        instance.property.department = instance.destination_department
        instance.property.save(update_fields=['department'])