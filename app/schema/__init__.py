from app import models
# from graphene_django import DjangoObjectType
import graphene
from graphql_jwt.decorators import login_required

from . import events_schema, products_schema, clients_schema, orders_schema, master_schema, feedback_schema, services_schema

# class OrderProductType(DjangoObjectType):
#     class Meta:
#         model = models.OrderProduct


# class OrderServiceType(DjangoObjectType):
#     class Meta:
#         model = models.OrderService

class Query(
    events_schema.Query,
    products_schema.Query,
    clients_schema.Query,
    orders_schema.Query,
    master_schema.Query,
    feedback_schema.Query,
    services_schema.Query,
    graphene.ObjectType
):
    all_categories = graphene.List(services_schema.CategoryType)
    all_breeds = graphene.List(services_schema.BreedType)
    # all_order_products = graphene.List(OrderProductType)
    # all_order_services = graphene.List(OrderServiceType)

    @login_required
    def resolve_all_categories(root, info, **kwargs):
        return models.Category.objects.all()

    @login_required
    def resolve_all_breeds(root, info, **kwargs):
        return models.Breed.objects.all()


class Mutation(
    events_schema.Mutation,
    products_schema.Mutation,
    clients_schema.Mutation,
    orders_schema.Mutation,
    master_schema.Mutation,
    feedback_schema.Mutation,
    services_schema.Mutation,
    graphene.ObjectType
):
    pass
