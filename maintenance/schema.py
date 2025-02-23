#maintenance/schema.py
import graphene
from graphene_django import DjangoObjectType
from maintenance.models import Maintenance

class MaintenanceType(DjangoObjectType):
    class Meta:
        model = Maintenance
        fields = "__all__"

class Query(graphene.ObjectType):
    all_maintenance = graphene.List(MaintenanceType)

    def resolve_all_maintenance(self, info):
        return Maintenance.objects.all()