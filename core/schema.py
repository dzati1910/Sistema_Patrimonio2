import graphene
from graphene_django.types import DjangoObjectType
from assets.models import Property, Movement
from maintenance.models import Maintenance # Ajuste os imports!

class PropertyType(DjangoObjectType):
    class Meta:
        model = Property

class MovementType(DjangoObjectType):
    class Meta:
        model = Movement

class MaintenanceType(DjangoObjectType):
    class Meta:
        model = Maintenance

class Query(graphene.ObjectType):
    all_properties = graphene.List(PropertyType)
    all_movements = graphene.List(MovementType)
    all_maintenance = graphene.List(MaintenanceType)

    def resolve_all_properties(self, info):
        return Property.objects.all()

    def resolve_all_movements(self, info):
        return Movement.objects.all()

    def resolve_all_maintenance(self, info):
        return Maintenance.objects.all()

schema = graphene.Schema(query=Query)
