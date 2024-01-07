from doctest import master
from django.utils.timezone import now
from app import models
from django.core.paginator import Paginator
from graphene_django import DjangoObjectType
import graphene
from graphql_jwt.decorators import login_required, superuser_required
import math

from .orders_schema import OrderType

class MasterType(DjangoObjectType):
    class Meta:
        model = models.Master

class MasterById(graphene.ObjectType):
    master = graphene.Field(MasterType)
    all_orders = graphene.List(OrderType)
    orders = graphene.List(OrderType)
    orders_size = graphene.Int()
    orders_pages_size = graphene.Int()

class MasterInputType(graphene.InputObjectType):
    username = graphene.String()
    lastname = graphene.String()
    phone = graphene.String()
    comment = graphene.String()
    education = graphene.String()
    post = graphene.String()
    color = graphene.String()
    address = graphene.String()
    rate = graphene.Int()


class CreateMaster(graphene.Mutation):
    class Arguments:
        master_data = MasterInputType(required=True)

    master = graphene.Field(MasterType)
    all_masters = graphene.List(MasterType)

    def mutate(
        self,
        root,
        master_data,
    ):
        user = root.context.user
        if not user.is_authenticated:
            raise Exception('Authentication credentials were not provided')

        for prop in ['username']:
            if not master_data[prop]:
                raise Exception('Missing main props')

        master = models.Master.objects.create(
            username=master_data.username,
            lastname=master_data.lastname or '',
            phone=master_data.phone or '',
            comment=master_data.comment or '',
            education=master_data.education or '',
            post=master_data.post or 'groommer',
            color=master_data.color or '#FFC11C',
            address=master_data.address or '',
            rate=master_data.rate or 0,
        )

        return CreateMaster(master=master, all_masters=models.Master.objects.all())


class UpdateMaster(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        master_data = MasterInputType(required=True)

    master = graphene.Field(MasterType)
    all_masters = graphene.List(MasterType)

    def mutate(
        self,
        root,
        id,
        master_data,
    ):
        user = root.context.user
        if not user.is_authenticated:
            raise Exception('Authentication credentials were not provided')

        master = models.Master.objects.get(pk=id)

        if (not master):
            raise Exception(f'Not master by ID = {id}')

        for key in master_data:
            if (key == 'post'):
                setattr(master, key, master_data[key].lower())
                continue

            setattr(master, key, master_data[key])

        master.update_date = now()
        master.save()

        return UpdateMaster(master=master, all_masters=models.Master.objects.all())


class RemoveMaster(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    master = graphene.Field(MasterType)
    all_masters = graphene.List(MasterType)
    success = graphene.Boolean()

    def mutate(
        self,
        root,
        id,
    ):
        user = root.context.user
        if not user.is_authenticated:
            raise Exception('Authentication credentials were not provided')

        master = models.Master.objects.get(pk=id)

        if (not master):
            raise Exception(f'Not master by ID = {id}')

        master.is_active = False
        master.save()

        return RemoveMaster(master=None, all_masters=models.Master.objects.all(), success=True)


class Query(graphene.ObjectType):
    all_groomers = graphene.List(MasterType)
    master_by_id = graphene.Field(
        MasterById,
        id=graphene.String(),
        orders_page=graphene.Int(),
        orders_per_page=graphene.Int(),
    )

    @login_required
    def resolve_all_clients(root, info, **kwargs):
        return models.Client.objects.all()

    @login_required
    def resolve_master_by_id(root, info, id, orders_page, orders_per_page):
        master_orders = models.Order.objects.filter(master__pk=id)
        paginator = Paginator(master_orders, orders_per_page or 15)
        orders_size = master_orders.count()
        orders_pages_size = orders_size / orders_per_page
        
        return {
            "master": models.Master.objects.get(pk=id) or None,
            "orders": paginator.get_page(orders_page),
            "orders_size": master_orders.count(),
            "orders_pages_size": math.ceil(orders_pages_size),
        }



class Mutation(graphene.ObjectType):
    create_master = CreateMaster.Field()
    update_master = UpdateMaster.Field()
    remove_master = RemoveMaster.Field()
