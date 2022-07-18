from app import models
from graphene_django import DjangoObjectType
import graphene

class ServiceType(DjangoObjectType):
    class Meta:
        model = models.Service

class Query(graphene.ObjectType):
    all_services = graphene.List(ServiceType)

    @graphene.resolve_only_args
    def resolve_all_services(self):
        return models.Service.objects.all()

schema = graphene.Schema(query=Query)
