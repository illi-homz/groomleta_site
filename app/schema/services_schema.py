from django.utils.timezone import now
from app import models
from graphene_django import DjangoObjectType
import graphene
from graphql_jwt.decorators import login_required, superuser_required


class CategoryType(DjangoObjectType):
    class Meta:
        model = models.Category


class BreedType(DjangoObjectType):
    class Meta:
        model = models.Breed


class ServiceType(DjangoObjectType):
    class Meta:
        model = models.Service

# class ClientById(graphene.ObjectType):
#     client = graphene.Field(ServiceType)
#     all_orders = graphene.List(OrderType)


class ServiceInputType(graphene.InputObjectType):
    title = graphene.String()
    text = graphene.String()
    animal = graphene.String()
    price = graphene.String()
    time = graphene.String()
    category = graphene.ID()
    breed = graphene.ID()


class CreateService(graphene.Mutation):
    class Arguments:
        service_data = ServiceInputType(required=True)

    service = graphene.Field(ServiceType)
    all_services = graphene.List(ServiceType)
    all_categories = graphene.List(CategoryType)
    all_breeds = graphene.List(BreedType)

    def mutate(
        self,
        root,
        service_data,
    ):
        user = root.context.user
        if not user.is_authenticated:
            raise Exception('Authentication credentials were not provided')

        for prop in ['title', 'animal', 'category', 'breed']:
            if not service_data[prop]:
                raise Exception(f'Missing main prop "{prop}"')

        current_animals = ['cat', 'dog', 'any']

        if not (service_data.animal in current_animals):
            raise Exception('Incorrect animal')

        service = models.Service.objects.create(
            title=service_data.title,
            text=service_data.text or '',
            animal=service_data.animal,
            price=service_data.price or '',
            time=service_data.time or '',
            category=models.Category.objects.get(pk=service_data.category),
            breed=models.Breed.objects.get(pk=service_data.breed),
        )

        return CreateService(
            service=service,
            all_services=models.Service.objects.all(),
            all_categories=models.Category.objects.all(),
            all_breeds=models.Breed.objects.all(),
        )


class UpdateService(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        service_data = ServiceInputType(required=True)

    service = graphene.Field(ServiceType)
    all_services = graphene.List(ServiceType)
    all_categories = graphene.List(CategoryType)
    all_breeds = graphene.List(BreedType)

    def mutate(
        self,
        root,
        id,
        service_data,
    ):
        user = root.context.user

        if not user.is_authenticated:
            raise Exception('Authentication credentials were not provided')

        service = models.Service.objects.get(pk=id)

        if (not service):
            raise Exception(f'Not service by ID = {id}')

        for key in service_data:
            data = None

            if key == 'category':
                data = models.Category.objects.get(
                    pk=service_data[key]) if service_data[key] else None
            elif key == 'breed':
                data = models.Breed.objects.get(
                    pk=service_data[key]) if service_data[key] else None
            else:
                data = service_data[key] or None

            setattr(service, key, data)

        service.save()

        return UpdateService(
            service=service,
            all_services=models.Service.objects.all(),
            all_categories=models.Category.objects.all(),
            all_breeds=models.Breed.objects.all(),
        )


class RemoveService(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(
        self,
        root,
        id,
    ):
        service = models.Service.objects.get(pk=id)

        if (not service):
            raise Exception(f'Not service by ID = {id}')

        service.is_active = False
        service.save()

        return RemoveService(
            success=True
        )


class AllServicesType(graphene.ObjectType):
    all_services = graphene.List(ServiceType)
    all_categories = graphene.List(CategoryType)
    all_breeds = graphene.List(BreedType)


class Query(graphene.ObjectType):
    # all_services = graphene.List(ServiceType)
    all_services = graphene.Field(AllServicesType)

    @login_required
    def resolve_all_services(root, info, **kwargs):
        # return models.Service.objects.all()
        return {
            "all_services": models.Service.objects.all(),
            "all_categories": models.Category.objects.all(),
            "all_breeds": models.Breed.objects.all(),
        }


class Mutation(graphene.ObjectType):
    create_service = CreateService.Field()
    update_service = UpdateService.Field()
    remove_service = RemoveService.Field()
