from app import models
from graphene_django import DjangoObjectType
import graphene
from graphql_jwt.decorators import login_required

from . import events_schema, products_schema, clients_schema

class ServiceType(DjangoObjectType):
    class Meta:
        model = models.Service

class CategoryType(DjangoObjectType):
    class Meta:
        model = models.Сategory

class BreedType(DjangoObjectType):
    class Meta:
        model = models.Breed

class MasterType(DjangoObjectType):
    class Meta:
        model = models.Master

class Query(events_schema.Query, products_schema.Query, clients_schema.Query, graphene.ObjectType):
    all_services = graphene.List(ServiceType)
    all_categories = graphene.List(CategoryType)
    all_breeds = graphene.List(BreedType)
    all_groomers = graphene.List(MasterType)
    groober_by_id = graphene.Field(MasterType, id=graphene.String())

    # @graphene.resolve_only_args
    @login_required
    def resolve_all_services(root, info, **kwargs):
        print('info.context.user.is_authenticated', info.context.user.is_authenticated)
        return models.Service.objects.all()

    @login_required
    def resolve_all_groomers(root, info, **kwargs):
        return models.Master.objects.all()

    @login_required
    def resolve_all_clients(root, info, **kwargs):
        return models.Client.objects.all()

    @login_required
    def resolve_all_breeds(root, info, **kwargs):
        return models.Breed.objects.all()

    @login_required
    def resolve_groober_by_id(root, info, id):
        return models.Master.objects.get(pk=id)

class Mutation(events_schema.Mutation, products_schema.Mutation, clients_schema.Mutation, graphene.ObjectType):
    pass
