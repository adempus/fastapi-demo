from fastapi import FastAPI
from tinydb import TinyDB, Query
from fastapi_demo.models import User, RoleEnum

app = FastAPI()
db = TinyDB("db/demo-db.json")
user_table = db.table("users")


@app.get("/")
def index():
    return {"Hello": "World"}


@app.post("/user/")
def create_user(user: User):
    user_id = user_table.insert(user.dict())
    user_query = Query()
    user_table.update({'id': user_id}, user_query.id == 0)
    user.id = user_id
    return user


@app.get("/user/{user_id}")
def read_user(user_id: int):
    user_query = Query()
    user = user_table.search(user_query.id == user_id)
    return user


@app.put("/user")
def update_user_role(user_id: int, role_id: int):
    user_query = Query()
    try:
        RoleEnum(role_id)
        user_table.update({'role': role_id}, user_query.id == user_id and user_query.role != 1)
        return user_table.search(user_query.id == user_id)
    except ValueError as err:
        print("invalid role provided")
        return {"error": err.__str__()}


@app.delete("/user")
def delete_user(user_id: int):
    user_query = Query()
    user = dict(*user_table.search(user_query.id == user_id))

    if len(user) == 0:
        return {"error": f"found no user with id: {user_id}"}
    if (user['role'] == 1):
        return {"error": "admin cannot be deleted"}
    else:
        user_table.remove(user_query.id == user_id)
        return {"success": True}

