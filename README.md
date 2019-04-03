# Flask + GraphQL + boilerplate

This is a Flask + GraphQL API boilerplate with JSON web token.

## Stack

- Flask
- GraphQL : Flask-GraphQL
- ORM : Flask-SQLAlchemy
- Password encryption : bcrypt
- Authentication: JSON web token
- DB : Postgres(psycopg2-binary)

## Feature

- GraphQL API
- User Sign Up / Sign In / Change password / Change profile
- JSON Web Token Authentication
- GraphiQL : Playground -> http://localhost:5000/graphql

## Configuration

### Dependencies

```shell
$ pip install -r requirements.txt
```

### `config.py`

```python
SQLALCHEMY_DATABASE_URI = 'postgres://<username>:<password>@<db_address = localhost>:5432/<db_name>'
SQLALCHEMY_TRACK_MODIFICATIONS = True
JWT_SECRET_KEY = 'secret'  # you must change this.
JWT_ACCESS_TOKEN_EXPIRES = 2592000
```

### Set a DB model

```python
# models.py

from app import db


class MyUser(db.Model):
    __tablename__ = 'myuser'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    firstname = db.Column(db.String(30), nullable=False)
    lastname = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String, nullable=False)
    bio = db.Column(db.String)
```

### DB initialization and migration

```shell
$ python db.py db init
```

```shell
$ python db.py db migrate
$ python db.py db upgrade
```

## Query

### Get Profile

> http request authorization headers -> Authorization: {token}

```graphql
query {
  me {
    ok
    error
    me {
      id
      email
      firstname
      lastname
      bio
      createdAt
      updatedAt
    }
  }
}
```

## Mutation

### Sign Up

```graphql
mutation {
  signUp(
    email: "flask@graphql.com"
    password: "12345678"
    firstname: "graphql"
    lastname: "flask"
  ) {
    ok
    error
    user {
      id
      email
      firstname
      lastname
      bio
    }
  }
}
```

### Sign In

```graphql
mutation {
  signIn(email: "flask@graphql.com", password: "12345678") {
    ok
    error
    token
  }
}
```

### Change Password

> http request authorization headers -> Authorization: {token}

```graphql
mutation {
  changeProfile(password: "87654321") {
    ok
    error
    user {
      id
      email
      firstname
      lastname
      bio
      createdAt
      updatedAt
    }
  }
}
```

### Change Profile

> http request authorization headers -> Authorization: {token}

```graphql
mutation {
  changeProfile(bio: "I'm flask user.") {
    ok
    error
    user {
      id
      email
      firstname
      lastname
      bio
      createdAt
      updatedAt
    }
  }
}
```

## Next to do

- [x] Sign Up
- [x] Sign In with JWT
- [x] Change profile
- [x] Change password
