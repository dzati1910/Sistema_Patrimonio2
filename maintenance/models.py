from django.db import models
from assets.models import Property


# Modelos do app maintenance

class Maintenance(models.Model):
    """
    Modelo que representa uma manutenção de um bem (property).
    Contém informações como data agendada, data de conclusão, custo, descrição e status.
    """

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        verbose_name="Bem",
        help_text="Bem que será submetido à manutenção."
    )
    scheduled_date = models.DateField(
        verbose_name="Data Agendada",
        help_text="Data em que a manutenção está agendada."
    )
    completion_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Data de Conclusão",
        help_text="Data em que a manutenção foi concluída (opcional)."
    )
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Custo",
        help_text="Custo total da manutenção."
    )
    description = models.TextField(
        null=True,
        blank=False,
        verbose_name="Descrição",
        help_text="Descrição detalhada da manutenção."
    )

    # Opções de status para a manutenção
    STATUS_CHOICES = [
        ('Agendado', 'Agendado'),
        ('Em Manutenção', 'Em Manutenção'),
        ('Completado', 'Completado'),
    ]
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='Agendado',
        verbose_name="Status",
        help_text="Status atual da manutenção."
    )

    def __str__(self):
        """Retorna uma representação legível da manutenção."""
        return f"Manutenção para {self.property.name} agendada em {self.scheduled_date}"

    def is_overdue(self):
        """
        Verifica se a manutenção está atrasada.
        Retorna True se a data agendada já passou e a manutenção não foi concluída.
        """
        from django.utils import timezone
        return self.scheduled_date < timezone.now().date() and not self.completion_date