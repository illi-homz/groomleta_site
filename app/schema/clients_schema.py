from django.utils.timezone import now
from app import models
from graphene_django import DjangoObjectType
import graphene
from django.core.paginator import Paginator
from graphql_jwt.decorators import login_required, superuser_required
import math

from .orders_schema import OrderType

class ClientType(DjangoObjectType):
    class Meta:
        model = models.Client
        orders = graphene.List(OrderType)
        orders_size = graphene.Int()
        orders_pages_size = graphene.Int()

class ClientById(graphene.ObjectType):
    client = graphene.Field(ClientType)
    orders = graphene.List(OrderType)
    orders_size = graphene.Int()
    orders_pages_size = graphene.Int()


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

        client.is_active = False
        client.save()

        return RemoveClient(client=None, all_clients=models.Client.objects.all(), success=True)


class PutToBlock(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    client = graphene.Field(ClientType)
    all_clients = graphene.List(ClientType)

    def mutate(
        self,
        root,
        id,
    ):
        client = models.Client.objects.get(pk=id)
        user = root.context.user

        if not user.is_authenticated:
            raise Exception('Authentication credentials were not provided')

        if (not client):
            raise Exception(f'Not client by ID = {id}')

        client.is_blocked = True
        client.update_date = now()

        client.save()

        return PutToBlock(client=client, all_clients=models.Client.objects.all())

class Query(graphene.ObjectType):
    all_clients = graphene.List(ClientType)
    client_by_id = graphene.Field(
        ClientById,
        id=graphene.String(),
        orders_page=graphene.Int(),
        orders_per_page=graphene.Int(),
    )

    @login_required
    def resolve_all_clients(root, info, **kwargs):
        return models.Client.objects.all()

    @login_required
    def resolve_client_by_id(root, info, id, orders_page, orders_per_page):
        client_orders = models.Order.objects.filter(client__pk=id)
        paginator = Paginator(client_orders, orders_per_page or 15)
        orders_size = client_orders.count()
        orders_pages_size = orders_size / orders_per_page

        return {
            "client": models.Client.objects.get(pk=id) or None,
            "orders": paginator.get_page(orders_page),
            "orders_size": client_orders.count(),
            "orders_pages_size": math.ceil(orders_pages_size),
        }



class Mutation(graphene.ObjectType):
    create_client = CreateClient.Field()
    update_client = UpdateClient.Field()
    remove_client = RemoveClient.Field()
    put_to_block = PutToBlock.Field()
