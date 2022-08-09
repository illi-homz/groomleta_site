from asyncio import events
from email.policy import default
from nis import match
from unittest import case
from app import models
from graphene_django import DjangoObjectType
import graphene
from graphql_jwt.decorators import login_required


class EventType(DjangoObjectType):
    class Meta:
        model = models.Event


class EventInputType(graphene.InputObjectType):
    title = graphene.String()
    start_date = graphene.DateTime()
    end_date = graphene.DateTime()
    services = graphene.List(graphene.ID)
    client = graphene.String()
    master = graphene.ID()
    comment = graphene.String()


class CreateEvent(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        start_date = graphene.DateTime(required=True)
        end_date = graphene.DateTime(required=True)
        services = graphene.List(graphene.ID, required=True)
        client = graphene.String()
        master = graphene.ID()
        comment = graphene.String()

    event = graphene.Field(EventType)

    def mutate(
        self,
        root,
        title,
        start_date,
        end_date,
        services,
        client,
        master,
        comment,
    ):
        event = models.Event.objects.create(
            title=title,
            start_date=start_date,
            end_date=end_date,
            comment=comment,
            client=models.Client.objects.get(pk=client) if client else None,
            master=models.Master.objects.get(pk=master) if master else None,
        )

        event.services.set(models.Service.objects.filter(id__in=services))

        return CreateEvent(event=event)


class UpdateEvent(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        event_data = EventInputType(required=True)

    event = graphene.Field(EventType)

    def mutate(
        self,
        root,
        id,
        event_data,
    ):
        event = models.Event.objects.get(pk=id)

        for key in event_data:
            data = None

            if key == 'client':
                data = models.Client.objects.get(pk=event_data[key])
            elif key == 'master':
                data = models.Master.objects.get(pk=event_data[key])
            elif key == 'services':
                data = models.Service.objects.filter(id__in=event_data[key])
                event.services.set(data)
                continue
            else:
                data = event_data[key]

            setattr(event, key, data)

        event.save()

        return UpdateEvent(event=event)


class Query(graphene.ObjectType):
    all_events = graphene.List(EventType)

    @login_required
    def resolve_all_events(root, info, **kwargs):
        return models.Event.objects.all()


class Mutation(graphene.ObjectType):
    create_event = CreateEvent.Field()
    update_event = UpdateEvent.Field()
