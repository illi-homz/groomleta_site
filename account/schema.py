from dataclasses import fields
from pyexpat import model
import graphene
import graphql_jwt
from django.contrib.auth.models import User
from graphene_django import DjangoObjectType
# from graphql_jwt.decorators import login_required

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class Query(graphene.ObjectType):
    user_details = graphene.List(UserType)

    def resolve_user_details(root, info, **kwargs):
        user = info.context.user

        if not user.is_authenticated:
            raise Exception('Authentication credentials were not provided')
        
        return User.objects.all()


class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()
