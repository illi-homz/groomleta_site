from app import models
from django.utils.timezone import now
from graphene_django import DjangoObjectType
import graphene
from graphql_jwt.decorators import login_required, superuser_required
import datetime


class EventType(DjangoObjectType):
    class Meta:
        model = models.Event


class EventInputType(graphene.InputObjectType):
    title = graphene.String()
    start_date = graphene.DateTime()
    end_date = graphene.DateTime()
    services = graphene.List(graphene.ID)
    client = graphene.ID()
    master = graphene.ID()
    comment = graphene.String()


class CreateEvent(graphene.Mutation):
    class Arguments:
        event_data = EventInputType(required=True)

    event = graphene.Field(EventType)
    all_events = graphene.List(EventType)

    def mutate(
        self,
        root,
        event_data,
    ):
        user = root.context.user
        if not user.is_authenticated:
            raise Exception('Authentication credentials were not provided')

        for prop in ['title', 'start_date', 'end_date']:
            if not event_data[prop]:
                raise Exception('Missing main props')

        event = models.Event.objects.create(
            title=event_data.title,
            start_date=event_data.start_date,
            end_date=event_data.end_date,
            comment=event_data.comment,
            client=models.Client.objects.get(
                pk=event_data.client) if event_data.client else None,
            master=models.Master.objects.get(
                pk=event_data.master) if event_data.master else None,
        )

        event.services.set(models.Service.objects.filter(
            id__in=event_data.services))

        return CreateEvent(event=event, all_events=models.Event.objects.all())


class UpdateEvent(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        event_data = EventInputType(required=True)

    event = graphene.Field(EventType)
    all_events = graphene.List(EventType)

    def mutate(
        self,
        root,
        id,
        event_data,
    ):
        event = models.Event.objects.get(pk=id)
        user = root.context.user
        if not user.is_authenticated:
            raise Exception('Authentication credentials were not provided')

        if (not event):
            raise Exception(f'Not event by ID = {id}')

        print('event_data', event_data)

        for key in event_data:
            data = None

            if key == 'master':
                data = models.Master.objects.get(
                    pk=event_data[key]) if event_data[key] else None
            elif key == 'client':
                data = models.Client.objects.get(pk=event_data[key]) if event_data[key] else None
            elif key == 'services':
                data = models.Service.objects.filter(id__in=event_data[key])
                event.services.set(data)
                continue
            else:
                data = event_data[key]

            setattr(event, key, data)

        event.update_date = now()

        event.save()

        return UpdateEvent(event=event, all_events=models.Event.objects.all())


class RemoveEvent(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    event = graphene.Field(EventType)
    all_events = graphene.List(EventType)

    def mutate(
        self,
        root,
        id,
    ):
        event = models.Event.objects.get(pk=id)

        if (not event):
            raise Exception(f'Not event by ID = {id}')

        event.delete()

        return RemoveEvent(event=None, all_events=models.Event.objects.all())

class SuccessEvent(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    event = graphene.Field(EventType)
    all_events = graphene.List(EventType)

    def mutate(
        self,
        root,
        id,
    ):
        event = models.Event.objects.get(pk=id)

        if (not event):
            raise Exception(f'Not event by ID = {id}')

        event.is_success = True
        event.save()

        return SuccessEvent(event=event, all_events=models.Event.objects.all())


class Query(graphene.ObjectType):
    all_events = graphene.List(EventType, year=graphene.String(), month=graphene.String())

    @login_required
    def resolve_all_events(root, info, year, month, **kwargs):
        today = datetime.date.today()
        year_default = today.year
        month_default = today.month

        return models.Event.objects.filter(
            start_date__year__gte=year or year_default,
            start_date__month__gte=month or month_default,
            start_date__year__lte=year or year_default,
            start_date__month__lte=month or month_default,
        )


class Mutation(graphene.ObjectType):
    create_event = CreateEvent.Field()
    update_event = UpdateEvent.Field()
    remove_event = RemoveEvent.Field()
    success_event = SuccessEvent.Field()
