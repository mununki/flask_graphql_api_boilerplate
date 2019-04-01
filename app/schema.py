import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from app import db
from app.models import MyUser


class MyUserType(SQLAlchemyObjectType):
    class Meta:
        model = MyUser


class Query(graphene.ObjectType):
    me = graphene.Field(MyUserType)

    def resolve_me(self, info):
        return {id: "1"}


class SignUp(graphene.Mutation):
    ok = graphene.Boolean()
    error = graphene.String()
    user = graphene.Field(MyUserType)

    class Arguments:
        email = graphene.String()
        password = graphene.String()
        firstname = graphene.String()
        lastname = graphene.String()

    def mutate(self, info, email, password, firstname, lastname, **kwargs):
        new_user = MyUser(email=email, password=password, firstname=firstname, lastname=lastname)
        new_user.set_password(password.encode('utf-8'))
        db.session.add(new_user)
        db.session.commit()
        return SignUp(ok=True, error=None, user=new_user)


class Mutation(graphene.ObjectType):
    sign_up = SignUp.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
