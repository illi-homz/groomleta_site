from app import models
from graphene_django import DjangoObjectType
import graphene
from graphql_jwt.decorators import login_required


class FeedbackType(DjangoObjectType):
    class Meta:
        model = models.Feedback


class FeedbackInputType(graphene.InputObjectType):
    is_approved = graphene.Boolean()


class UpdateFeedback(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        feedback_data = FeedbackInputType(required=True)

    feedback = graphene.Field(FeedbackType)
    all_feedbacks = graphene.List(FeedbackType)

    def mutate(
        self,
        root,
        id,
        feedback_data,
    ):
        feedback = models.Feedback.objects.get(pk=id)
        user = root.context.user
        if not user.is_authenticated:
            raise Exception('Authentication credentials were not provided')

        if (not feedback):
            raise Exception(f'Not feedback by ID = {id}')

        feedback.is_approved = feedback_data.is_approved

        feedback.save()

        return UpdateFeedback(feedback=feedback, all_feedbacks=models.Feedback.objects.all())


class Query(graphene.ObjectType):
    all_feedbacks = graphene.List(FeedbackType)

    @login_required
    def resolve_all_feedbacks(root, info, **kwargs):
        return models.Feedback.objects.all()


class Mutation(graphene.ObjectType):
    update_feedback = UpdateFeedback.Field()
