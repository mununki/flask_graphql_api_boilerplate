# Flask + GraphQL + boilerplate

This is a basic api boilerplate with Flask + GraphQL.

## Stack

- Flask
- ORM : Flask-SQLAlchemy
- Password encryption : bcrypt
- GraphQL : Flask-GraphQL
- DB : psycopg2-binary

## Feature

- GraphQL API
- User Sign Up / Sign In / Change password / Change profile
- JSON Web Token

## DB Initialization

### `config.py`

```python
SQLALCHEMY_DATABASE_URI = 'postgres://<username>:<password>@<db_address = localhost>:5432/<db_name>'
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

### Initialize

```shell
$ python db.py db init
```

## DB Migration

```shell
$ python db.py db migrate
$ python db.py db upgrade
```

## Query

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

## Next to do

- [x] Sign Up
- [ ] Sign In with JWT
- [ ] Change password
- [ ] Change profile
