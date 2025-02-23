from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone


# Modelos do app contacts

class Supplier(models.Model):
    """
    Modelo que representa um fornecedor no sistema.
    Contém informações como nome, CNPJ (tax_id) e contato.
    """

    name = models.CharField(max_length=200, verbose_name="Nome")
    tax_id = models.CharField(
        max_length=14,
        unique=True,
        verbose_name="CNPJ",
        validators=[
            RegexValidator(
                r'^\d{14}$',
                'O campo deve conter exatamente 14 dígitos numéricos'
            )
        ],
    )
    contact = models.CharField(
        max_length=14,
        verbose_name="Contato",
        validators=[
            RegexValidator(
                r'^\d{14}$',
                'O campo deve conter exatamente 14 dígitos numéricos'
            )
        ],
        unique=True,
    )

    def __str__(self):
        """Retorna o nome do fornecedor."""
        return self.name

    @property
    def active_contracts(self):
        """
        Retorna a quantidade de contratos ativos associados a este fornecedor.
        Um contrato é considerado ativo se a data atual estiver entre a data de início e a data de término.
        """
        today = timezone.now().date()
        return self.contract_set.filter(
            start_date__lte=today,
            end_date__gte=today
        ).count()