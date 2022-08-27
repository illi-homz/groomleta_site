from django.utils.timezone import now
from app import models
from graphene_django import DjangoObjectType
import graphene
from graphql_jwt.decorators import login_required, superuser_required


class ProductType(DjangoObjectType):
    class Meta:
        model = models.Product


class ProductInputType(graphene.InputObjectType):
    title = graphene.String()
    vendor_code = graphene.String()
    count = graphene.Int()
    price = graphene.Int()
    description = graphene.String()


class CreateProduct(graphene.Mutation):
    class Arguments:
        product_data = ProductInputType(required=True)

    product = graphene.Field(ProductType)
    all_products = graphene.List(ProductType)

    def mutate(
        self,
        root,
        product_data,
    ):
        user = root.context.user
        if not user.is_authenticated:
            raise Exception('Authentication credentials were not provided')

        for prop in ['title']:
            if not product_data[prop]:
                raise Exception('Missing main props')

        product = models.Product.objects.create(
            title=product_data.title,
            vendor_code=product_data.vendor_code or '',
            count=product_data.count or 0,
            price=product_data.price or 0,
            description=product_data.description or '',
        )

        return CreateProduct(product=product, all_products=models.Product.objects.all())


class UpdateProduct(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        product_data = ProductInputType(required=True)

    product = graphene.Field(ProductType)
    all_products = graphene.List(ProductType)

    def mutate(
        self,
        root,
        id,
        product_data,
    ):
        product = models.Product.objects.get(pk=id)
        user = root.context.user
        if not user.is_authenticated:
            raise Exception('Authentication credentials were not provided')

        if (not product):
            raise Exception(f'Not product by ID = {id}')

        for key in product_data:
            setattr(product, key, product_data[key])

        product.update_date = now()

        product.save()

        return UpdateProduct(product=product, all_products=models.Product.objects.all())


class RemoveProduct(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    product = graphene.Field(ProductType)
    all_products = graphene.List(ProductType)
    success = graphene.Boolean()

    def mutate(
        self,
        root,
        id,
    ):
        product = models.Product.objects.get(pk=id)

        if (not product):
            raise Exception(f'Not product by ID = {id}')

        product.delete()

        return RemoveProduct(product=None, all_products=models.Product.objects.all(), success=True)


class Query(graphene.ObjectType):
    all_products = graphene.List(ProductType)

    @login_required
    def resolve_all_products(root, info, **kwargs):
        return models.Product.objects.all()


class Mutation(graphene.ObjectType):
    create_product = CreateProduct.Field()
    update_product = UpdateProduct.Field()
    remove_product = RemoveProduct.Field()
