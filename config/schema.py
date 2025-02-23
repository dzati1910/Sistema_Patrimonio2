# config/schema.py
import graphene
from assets.schema import Query as AssetQuery
from movements.schema import Query as MovementQuery
from maintenance.schema import Query as MaintenanceQuery

class Query(
    AssetQuery,  # Traz only_properties (se necessário)
    MovementQuery,  # Traz all_movements
    MaintenanceQuery,  # Traz all_maintenance
    graphene.ObjectType
):
    pass


schema = graphene.Schema(query=Query)