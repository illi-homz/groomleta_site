from itertools import product
from app import models
from django.utils.timezone import now
from graphene_django import DjangoObjectType
import graphene
from graphql_jwt.decorators import login_required, superuser_required


class OrderType(DjangoObjectType):
    class Meta:
        model = models.Order

class OrderProductInputType(graphene.InputObjectType):
    id = graphene.ID()
    product_id = graphene.ID()
    count = graphene.Int()

class OrderServiceInputType(graphene.InputObjectType):
    id = graphene.ID()
    service_id = graphene.ID()
    count = graphene.Int()

class OrderInputType(graphene.InputObjectType):
    price = graphene.Int()
    products = graphene.List(OrderProductInputType)
    master = graphene.ID()
    client = graphene.ID()
    services = graphene.List(OrderServiceInputType)
    is_success = graphene.Boolean()


class CreateOrder(graphene.Mutation):
    class Arguments:
        order_data = OrderInputType(required=True)

    order = graphene.Field(OrderType)

    def mutate(
        self,
        root,
        order_data,
    ):
        user = root.context.user
        if not user.is_authenticated:
            raise Exception('Authentication credentials were not provided')

        products = []
        services = []

        print(order_data)

        if len(order_data.products):
            for prod in order_data.products:
                product_obj = models.Product.objects.get(
                    pk=prod.product_id)
                
                print('product_obj', product_obj)
                if product_obj:
                    product = models.OrderProduct.objects.create(
                        count=prod.count or 0,
                        product=product_obj
                    )
                    print('product', product)
                    products.append(product)

        if len(order_data.services):
            for serv in order_data.services:
                service_obj = models.Service.objects.get(
                    pk=serv.service_id)
                
                if service_obj:
                    service = models.OrderService.objects.create(
                        count=serv.count or 0,
                        service=service_obj
                    )
                    services.append(service)

        order = models.Order.objects.create(
            price=order_data.price or 0,
            is_success=order_data.is_success or False,
            client=models.Client.objects.get(
                pk=order_data.client) if order_data.client else None,
            master=models.Master.objects.get(
                pk=order_data.master) if order_data.master else None,
        )

        if len(products):
            order.products.set(products)

        if len(services):
            order.services.set(services)

        return CreateOrder(order=order)

class PayOrder(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    order = graphene.Field(OrderType)

    def mutate(
        self,
        root,
        id,
    ):
        user = root.context.user
        if not user.is_authenticated:
            raise Exception('Authentication credentials were not provided')

        order = models.Order.objects.get(pk=id)
        order.is_success = True
        order.update_date = now()

        return CreateOrder(order=order, success=True)

class CancelOrder(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    order = graphene.Field(OrderType)

    def mutate(
        self,
        root,
        id,
    ):
        user = root.context.user
        if not user.is_authenticated:
            raise Exception('Authentication credentials were not provided')

        order = models.Order.objects.get(pk=id)
        order.is_cancel = True
        order.update_date = now()

        return CreateOrder(order=order, success=True)

class Query(graphene.ObjectType):
    all_orders = graphene.List(OrderType)

    @login_required
    def resolve_all_orders(root, info, **kwargs):
        return models.Order.objects.all()


class Mutation(graphene.ObjectType):
    create_order = CreateOrder.Field()
    pay_order = PayOrder.Field()
    cancel_order = CancelOrder.Field()
