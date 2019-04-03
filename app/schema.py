import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, decode_token)
from functools import wraps

from app import db
from app import jwt
from app.models import MyUser


def signin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            user_id = decode_token(args[1].context.headers.get('authorization'))['identity']
        except Exception:
            user_id = None
        if user_id:
            args = list(args)
            args.append(user_id)
            args = tuple(args)
        return fn(*args, **kwargs)
    return wrapper


class MyUserType(SQLAlchemyObjectType):
    class Meta:
        model = MyUser


class GetMyProfile(graphene.ObjectType):
    ok = graphene.Boolean()
    error = graphene.String()
    me = graphene.Field(MyUserType)


class Query(graphene.ObjectType):
    me = graphene.Field(GetMyProfile)

    @signin_required
    def resolve_me(self, info, user_id=None):
        if user_id:
            user = MyUser.query.filter_by(id=user_id).first()
            if user:
                return GetMyProfile(ok=True, error=None, me=user)
            else:
                return GetMyProfile(ok=False, error="Not existing user", me=None)
        else:
            return GetMyProfile(ok=False, error="Login Required", me=None)


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


class ChangeProfileResponse(graphene.Mutation):
    ok = graphene.Boolean()
    error = graphene.String()
    user = graphene.Field(MyUserType)

    class Arguments:
        bio = graphene.String()

    @signin_required
    def mutate(self, info, user_id=None, bio=None, **kwargs):
        if user_id:
            user = MyUser.query.filter_by(id=user_id).first()
            if user:
                user.bio = bio
                db.session.commit()
                return ChangeProfileResponse(ok=True, error=None, user=user)
            else:
                return ChangeProfileResponse(ok=False, error="Not existing user", user=None)
        else:
            return ChangeProfileResponse(ok=False, error="Login required", user=None)
            



class Mutation(graphene.ObjectType):
    sign_up = SignUpResponse.Field()
    sign_in = SignInResponse.Field()
    change_profile = ChangeProfileResponse.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
