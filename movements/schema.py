#movements/schema.py
import graphene
from graphene_django import DjangoObjectType

from assets.models import Property, Department
from movements.models import Movement
from graphene import Mutation, String, ID, Field

# Define the GraphQL object type for Movement
class MovementType(DjangoObjectType):
    class Meta:
        model = Movement
        fields = ("id", "property", "origin_department", "destination_department", "timestamp")

# Define the Query type for Movements
class Query(graphene.ObjectType):
    all_movements = graphene.List(MovementType)
    movement = graphene.Field(MovementType, id=graphene.ID(required=True))

    def resolve_all_movements(self, info):
        return Movement.objects.all()

    def resolve_movement(self, info, id):
        try:
            return Movement.objects.get(pk=id)
        except Movement.DoesNotExist:
            return None

# Define the Mutation type for Movements
class CreateMovement(Mutation):
    movement = Field(MovementType)

    class Arguments:
        property_id = ID(required=True)
        origin_department_id = ID(required=True)
        destination_department_id = ID(required=True)

    def mutate(self, info, property_id, origin_department_id, destination_department_id):
        # Fetch related objects
        property = Property.objects.get(pk=property_id)
        origin_department = Department.objects.get(pk=origin_department_id)
        destination_department = Department.objects.get(pk=destination_department_id)

        # Create Movement instance
        movement = Movement(
            property=property,
            origin_department=origin_department,
            destination_department=destination_department
        )

        # Validate using Django's built-in methods
        movement.full_clean()
        movement.save()

        return CreateMovement(movement=movement)

class Mutation(graphene.ObjectType):
    create_movement = CreateMovement.Field()