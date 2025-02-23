# assets/schema.py
import graphene
from graphene_django import DjangoObjectType
from assets.models import Property, Department
from maintenance.schema import MaintenanceType
from movements.schema import MovementType


class PropertyType(DjangoObjectType):
    class Meta:
        model = Property
        fields = "__all__"

class DepartmentType(DjangoObjectType):
    class Meta:
        model = Department
        fields = "__all__"

class Query(graphene.ObjectType):
    all_properties = graphene.List(PropertyType)  # Correto

    def resolve_all_properties(self, info):
        return Property.objects.all()

    def resolve_all_departments(self, info):
        return Department.objects.all()