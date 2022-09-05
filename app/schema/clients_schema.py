from django.utils.timezone import now
from app import models
from graphene_django import DjangoObjectType
import graphene
from graphql_jwt.decorators import login_required, superuser_required

from .orders_schema import OrderType

class ClientType(DjangoObjectType):
    class Meta:
        model = models.Client

class ClientById(graphene.ObjectType):
    client = graphene.Field(ClientType)
    all_orders = graphene.List(OrderType)


class ClientInputType(graphene.InputObjectType):
    username = graphene.String()
    lastname = graphene.String()
    phone = graphene.String()
    comment = graphene.String()
    animal = graphene.String()
    address = graphene.String()


class CreateClient(graphene.Mutation):
    class Arguments:
        client_data = ClientInputType(required=True)

    client = graphene.Field(ClientType)
    all_clients = graphene.List(ClientType)

    def mutate(
        self,
        root,
        client_data,
    ):
        user = root.context.user
        if not user.is_authenticated:
            raise Exception('Authentication credentials were not provided')

        for prop in ['username']:
            if not client_data[prop]:
                raise Exception('Missing main props')

        client = models.Client.objects.create(
            username=client_data.username,
            lastname=client_data.lastname or '',
            phone=client_data.phone or '',
            comment=client_data.comment or '',
            animal=client_data.animal or '',
            address=client_data.address or '',
        )

        return CreateClient(client=client, all_clients=models.Client.objects.all())


class UpdateClient(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        client_data = ClientInputType(required=True)

    client = graphene.Field(ClientType)
    all_clients = graphene.List(ClientType)

    def mutate(
        self,
        root,
        id,
        client_data,
    ):
        client = models.Client.objects.get(pk=id)
        user = root.context.user
        if not user.is_authenticated:
            raise Exception('Authentication credentials were not provided')

        if (not client):
            raise Exception(f'Not client by ID = {id}')

        for key in client_data:
            setattr(client, key, client_data[key] or None)

        client.update_date = now()

        client.save()

        return UpdateClient(client=client, all_clients=models.Client.objects.all())


class RemoveClient(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    client = graphene.Field(ClientType)
    all_clients = graphene.List(ClientType)
    success = graphene.Boolean()

    def mutate(
        self,
        root,
        id,
    ):
        client = models.Client.objects.get(pk=id)

        if (not client):
            raise Exception(f'Not client by ID = {id}')

        client.delete()

        return RemoveClient(client=None, all_clients=models.Client.objects.all(), success=True)


class Query(graphene.ObjectType):
    all_clients = graphene.List(ClientType)
    client_by_id = graphene.Field(ClientById, id=graphene.String())

    @login_required
    def resolve_all_clients(root, info, **kwargs):
        return models.Client.objects.all()

    @login_required
    def resolve_client_by_id(root, info, id):
        return {
            "client": models.Client.objects.get(pk=id) or None,
            "all_orders": models.Order.objects.filter(client__pk=id)
        }



class Mutation(graphene.ObjectType):
    create_client = CreateClient.Field()
    update_client = UpdateClient.Field()
    remove_client = RemoveClient.Field()
