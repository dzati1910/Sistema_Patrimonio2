from django.contrib.auth.models import AbstractUser
from django.db import models
from assets.models import Department


# Modelos do app core

class User(AbstractUser):
    """
    Modelo personalizado de usuário que estende o AbstractUser do Django.
    Adiciona um campo para CPF (tax_id) e métodos relacionados ao departamento.
    """

    tax_id = models.CharField(
        max_length=11,
        unique=True,
        blank=True,
        null=True,
        verbose_name="CPF"
    )

    def __str__(self):
        """Retorna o nome de usuário como representação do objeto."""
        return self.username

    def is_department_responsible(self):
        """
        Verifica se o usuário é responsável por algum departamento.
        Retorna True se o usuário for responsável por pelo menos um departamento.
        """
        return Department.objects.filter(responsible_person=self).exists()


class SalesData(models.Model):
    """
    Modelo para armazenar dados de vendas.
    Contém informações como data, valor e região da venda.
    """

    date = models.DateField(verbose_name="Data da Venda")
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Valor da Venda"
    )
    region = models.CharField(max_length=100, verbose_name="Região")

    def __str__(self):
        """Retorna uma representação legível dos dados de venda."""
        return f"Venda em {self.date} - {self.region} - R${self.amount}"