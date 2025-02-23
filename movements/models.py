# movements/models.py
from django.db import models
from django.core.exceptions import ValidationError


class Movement(models.Model):
    """
    Modelo que representa um movimento de um bem (property) entre departamentos.
    Contém informações sobre o bem, o departamento de origem, o departamento de destino
    e o horário em que o movimento foi registrado.
    """

    property = models.ForeignKey(
        'assets.Property',
        on_delete=models.CASCADE,
        verbose_name="Bem",
        help_text="Bem que está sendo movimentado."
    )
    origin_department = models.ForeignKey(
        'assets.Department',
        on_delete=models.CASCADE,
        related_name="origin_movements",
        verbose_name="Departamento de Origem",
        help_text="Departamento de onde o bem está sendo movido."
    )
    destination_department = models.ForeignKey(
        'assets.Department',
        on_delete=models.CASCADE,
        related_name="destination_movements",
        verbose_name="Departamento de Destino",
        help_text="Departamento para onde o bem está sendo movido."
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data e Hora",
        help_text="Data e hora em que o movimento foi registrado."
    )

    def __str__(self):
        """Retorna uma representação legível do movimento."""
        return f"{self.property} movido de {self.origin_department} para {self.destination_department}"

    def save(self, *args, **kwargs):
        """
        Salva o movimento no banco de dados.
        As validações foram movidas para o formulário correspondente.
        """
        super().save(*args, **kwargs)