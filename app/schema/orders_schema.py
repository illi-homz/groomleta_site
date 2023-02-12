from itertools import product
from app import models
from datetime import datetime, timedelta
from django.utils.timezone import now
from django.core.paginator import Paginator
from django.db.models.functions import Ceil
from graphene_django import DjangoObjectType
import graphene
from graphql_jwt.decorators import login_required, superuser_required
import math

class OrderType(DjangoObjectType):
    class Meta:
        model = models.Order

class OrderWithPaginationType(graphene.ObjectType):
    nodes = graphene.List(OrderType)
    nodes_size = graphene.Int()
    page_count = graphene.Int()

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
    is_reserved = graphene.Boolean()


class CreateOrder(graphene.Mutation):
    class Arguments:
        order_data = OrderInputType(required=True)

    order = graphene.Field(OrderType)
    all_orders = graphene.List(OrderType)

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

                    product_obj.count = product_obj.count - prod.count
                    product_obj.save()

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

        is_success = order_data.is_success or False

        order = models.Order.objects.create(
            price=order_data.price or 0,
            is_success=is_success,
            is_reserved=False if is_success else order_data.is_reserved or True,
            client=models.Client.objects.get(
                pk=order_data.client) if order_data.client else None,
            master=models.Master.objects.get(
                pk=order_data.master) if order_data.master else None,
        )

        if len(products):
            order.products.set(products)

        if len(services):
            order.services.set(services)

        return CreateOrder(order=order, all_orders=models.Order.objects.all())


class PayForOrder(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    order = graphene.Field(OrderType)
    all_orders = graphene.List(OrderType)

    def mutate(
        self,
        root,
        id,
    ):
        print('id', id)
        user = root.context.user
        if not user.is_authenticated:
            raise Exception('Authentication credentials were not provided')

        order = models.Order.objects.get(pk=id)
        order.is_success = True
        order.update_date = now()
        order.save()

        return PayForOrder(order=order, all_orders=models.Order.objects.all())


def cancelProductsCount(order):
    for product in order.products.all():
        prodObj = models.Product.objects.get(pk=product.product_id)
        prodObj.count = prodObj.count + product.count
        prodObj.save()

def checkOrders():
    orders = models.Order.objects.filter(is_reserved=True, is_success=False, is_cancel=False)

    for order in orders:
        create_date = order.create_date
        now = datetime.now()
        create_timedelta = now - create_date

        if create_timedelta > timedelta(days=1):
            cancelProductsCount(order)
            order.delete()

class UpdateAndPayOrder(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        order_data = OrderInputType(required=True)

    order = graphene.Field(OrderType)
    all_orders = graphene.List(OrderType)

    def mutate(
        self,
        root,
        id,
        order_data,
    ):
        user = root.context.user
        if not user.is_authenticated:
            raise Exception('Authentication credentials were not provided')

        order = models.Order.objects.select_for_update().get(pk=id)

        cancelProductsCount(order)

        products = []
        services = []

        if len(order_data.products):
            for prod in order_data.products:
                product_obj = models.Product.objects.get(
                    pk=prod.product_id
                )
                order_product = models.OrderProduct.objects.get(
                    pk=prod.id
                ) if prod.id else None

                if order_product:
                    order_product.count = prod.count
                    order_product.save()
                    products.append(order_product)
                else:
                    if not product_obj:
                        continue

                    product = models.OrderProduct.objects.create(
                        count=prod.count or 0,
                        product=product_obj
                    )
                    products.append(product)

                product_obj.count = product_obj.count - prod.count
                product_obj.save()

        if len(order_data.services):
            for serv in order_data.services:
                order_service = models.OrderService.objects.get(
                    pk=serv.id
                ) if serv.id else None

                if order_service:
                    order_service.count = serv.count
                    order_service.save()
                    services.append(order_service)
                    continue

                service_obj = models.Service.objects.get(
                    pk=serv.service_id)

                if service_obj:
                    service = models.OrderService.objects.create(
                        count=serv.count or 0,
                        service=service_obj
                    )
                    services.append(service)

        if len(products):
            order.products.set(products)

        if len(services):
            order.services.set(services)

        order.master=models.Master.objects.get(
                pk=order_data.master) if order_data.master else None
        order.client = models.Client.objects.get(
            pk=order_data.client) if order_data.client else None
        order.price = order_data.price or 0
        order.is_success = True
        order.save()

        return UpdateAndPayOrder(order=order, all_orders=models.Order.objects.all())


class CancelOrder(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    order = graphene.Field(OrderType)
    all_orders = graphene.List(OrderType)

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

        cancelProductsCount(order)

        order.save()

        return CancelOrder(order=order, all_orders=models.Order.objects.all())

class Query(graphene.ObjectType):
    all_orders = graphene.List(OrderType)
    orders = graphene.Field(
        OrderWithPaginationType,
        page=graphene.Int(),
        objects_per_page=graphene.Int(),
        sort=graphene.String(),
    )

    @login_required
    def resolve_all_orders(root, info, **kwargs):
        checkOrders()
            

        return models.Order.objects.all()

    @login_required
    def resolve_orders(root, info, page, objects_per_page, sort, **kwargs):
        checkOrders()

        key = Ceil('pk')
        sortBy = key.asc() if sort == 'asc' else key.desc()
        orders = models.Order.objects.order_by(sortBy)
        paginator = Paginator(orders, objects_per_page or 15)
        nodes_size = models.Order.objects.all().count()
        page_count = nodes_size / objects_per_page

        return {
            'nodes': paginator.get_page(page),
            'nodes_size': nodes_size,
            'page_count': math.ceil(page_count)
        }


class Mutation(graphene.ObjectType):
    create_order = CreateOrder.Field()
    pay_for_order = PayForOrder.Field()
    cancel_order = CancelOrder.Field()
    update_and_pay_order = UpdateAndPayOrder.Field()

