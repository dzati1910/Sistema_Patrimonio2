from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Movement


@receiver(post_save, sender=Movement)
def update_property_department(sender, instance, created, **kwargs):
    """
    Signal que atualiza o departamento de um bem (property) após a criação de um movimento.
    O departamento do bem é atualizado para o departamento de destino do movimento.
    A atualização ocorre apenas se o movimento for novo (created=True) e se o departamento
    de destino for diferente do departamento atual do bem.
    """
    if created:  # Só atualiza se for um novo movimento
        property = instance.property
        if property.department != instance.destination_department:
            property.department = instance.destination_department
            property.save(update_fields=['department'])