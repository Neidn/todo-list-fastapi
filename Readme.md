# Todo List FastAPI

## Description

This is a simple todo list API using FastAPI and SQLite.
DB is easy to change to any other SQL DB.

## Installation

1. Clone the repository
2. Install the requirements
3. Run the server

```bash
git clone
cd todo-list-fastapi
pip install -r requirements.txt
make run
```

## Usage

### Create a new user

```bash
curl -X 'POST' \
    'http://localhost:8000/api/v1/user' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json
    -d '{
    "username": "string",
    "email": "string",
    "full_name": "string",
    "plain_password": "string",
    "repeat_plain_password": "string"
    }'
```

### Sign In And Get Token

Example scope: `TODOS/GET TODOS/GET/{todo_id} TODOS/POST/{todo_id} TODOS/PUT/{todo_id} TODOS/DELETE/{todo_id}`

```bash
curl -X 'POST' \
    'http://localhost:8000/api/v1/token' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    -d 'username=string&password=string&scope=string'
```

### Create a new todo

```bash
curl -X 'POST' \
    'http://localhost:8000/api/v1/todos' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -H 'Authorization: Bearer <token>' \
    -d '{
    "title": "string",
    "content": "string",
    "is_done": boolean,
    }'
```

### Get all todos

```bash
curl -X 'GET' \
    'http://localhost:8000/api/v1/todos' \
    -H 'accept: application/json' \
    -H 'Authorization: Bearer <token>'
```

### Get a todo by id

```bash
curl -X 'GET' \
    'http://localhost:8000/api/v1/todos/{todo_id}' \
    -H 'accept: application/json' \
    -H 'Authorization: Bearer <token>'
```

### Update a todo by id

```bash
curl -X 'PUT' \
    'http://localhost:8000/api/v1/todos/{todo_id}' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -H 'Authorization: Bearer <token>' \
    -d '{
    "title": "string",
    "content": "string",
    "is_done": boolean,
    }'
```

### Delete a todo by id

```bash
curl -X 'DELETE' \
    'http://localhost:8000/api/v1/todos/{todo_id}' \
    -H 'accept: application/json' \
    -H 'Authorization: Bearer <token>'
```


