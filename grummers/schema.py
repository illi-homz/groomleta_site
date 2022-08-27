import graphene
import app.schema
import account.schema

class Query(app.schema.Query, account.schema.Query, graphene.ObjectType):
    pass

class Mutation(app.schema.Mutation, account.schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
