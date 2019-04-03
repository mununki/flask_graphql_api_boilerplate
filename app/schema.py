import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity)

from app import db
from app import jwt
from app.models import MyUser


class MyUserType(SQLAlchemyObjectType):
    class Meta:
        model = MyUser


class Query(graphene.ObjectType):
    me = graphene.Field(MyUserType)

    def resolve_me(self, info):
        return {id: "1"}


class SignUpResponse(graphene.Mutation):
    ok = graphene.Boolean()
    error = graphene.String()
    user = graphene.Field(MyUserType)

    class Arguments:
        email = graphene.String()
        password = graphene.String()
        firstname = graphene.String()
        lastname = graphene.String()

    def mutate(self, info, email, password, firstname, lastname, **kwargs):
        user = MyUser.query.filter_by(email=email).first()
        if user:
            return SignUpResponse(ok=False, error="Already signed up", user=None)
        else:
            new_user = MyUser(email=email, password=password, firstname=firstname, lastname=lastname)
            new_user.set_password(password.encode('utf-8'))
            db.session.add(new_user)
            db.session.commit()
            return SignUpResponse(ok=True, error=None, user=new_user)


class SignInResponse(graphene.Mutation):
    ok = graphene.Boolean()
    error = graphene.String()
    token = graphene.String()

    class Arguments:
        email = graphene.String()
        password = graphene.String()

    def mutate(self, info, email, password, **kwargs):
        user = MyUser.query.filter_by(email=email).first()
        if user:
            if user.check_password(password):
                token = create_access_token(identity=user.id)
                return SignInResponse(ok=True, error=None, token=token)
            else:
                return SignInResponse(ok=False, error="Wrong password", token=None)
        else:
            return SignInResponse(ok=False, error="Not existing user", token=None)


class Mutation(graphene.ObjectType):
    sign_up = SignUpResponse.Field()
    sign_in = SignInResponse.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
