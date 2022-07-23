from app import models
from graphene_django import DjangoObjectType
import graphene
from graphql_jwt.decorators import login_required

class ServiceType(DjangoObjectType):
    class Meta:
        model = models.Service

class Query(graphene.ObjectType):
    all_services = graphene.List(ServiceType)

    # @graphene.resolve_only_args
    @login_required
    def resolve_all_services(root, info, **kwargs):
        return models.Service.objects.all()
