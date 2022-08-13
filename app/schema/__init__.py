from app import models
from graphene_django import DjangoObjectType
import graphene
from graphql_jwt.decorators import login_required

from . import events_schema, products_schema, clients_schema, orders_schema, master_schema


class ServiceType(DjangoObjectType):
    class Meta:
        model = models.Service


class CategoryType(DjangoObjectType):
    class Meta:
        model = models.Сategory


class BreedType(DjangoObjectType):
    class Meta:
        model = models.Breed

class OrderProductType(DjangoObjectType):
    class Meta:
        model = models.OrderProduct


class OrderServiceType(DjangoObjectType):
    class Meta:
        model = models.OrderService


class Query(
    events_schema.Query,
    products_schema.Query,
    clients_schema.Query,
    orders_schema.Query,
    master_schema.Query,
    graphene.ObjectType
):
    all_services = graphene.List(ServiceType)
    all_categories = graphene.List(CategoryType)
    all_breeds = graphene.List(BreedType)
    all_order_products = graphene.List(OrderProductType)
    all_order_services = graphene.List(OrderServiceType)

    # @graphene.resolve_only_args
    @login_required
    def resolve_all_services(root, info, **kwargs):
        print('info.context.user.is_authenticated',
              info.context.user.is_authenticated)
        return models.Service.objects.all()

    @login_required
    def resolve_all_groomers(root, info, **kwargs):
        return models.Master.objects.all()

    @login_required
    def resolve_all_breeds(root, info, **kwargs):
        return models.Breed.objects.all()

class Mutation(
    events_schema.Mutation,
    products_schema.Mutation,
    clients_schema.Mutation,
    orders_schema.Mutation,
    master_schema.Mutation,
    graphene.ObjectType
):
    pass
