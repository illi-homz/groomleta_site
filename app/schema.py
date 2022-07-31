from app import models
from graphene_django import DjangoObjectType
import graphene
from graphql_jwt.decorators import login_required

class ServiceType(DjangoObjectType):
    class Meta:
        model = models.Service

class MasterType(DjangoObjectType):
    class Meta:
        model = models.Master

class Query(graphene.ObjectType):
    all_services = graphene.List(ServiceType)
    all_groomers = graphene.List(MasterType)
    groober_by_id = graphene.Field(MasterType, id=graphene.String())

    # @graphene.resolve_only_args
    @login_required
    def resolve_all_services(root, info, **kwargs):
        return models.Service.objects.all()

    @login_required
    def resolve_all_groomers(root, info, **kwargs):
        return models.Master.objects.all()

    @login_required
    def resolve_groober_by_id(root, info, id):
        # Querying a single question
        return models.Master.objects.get(pk=id)
