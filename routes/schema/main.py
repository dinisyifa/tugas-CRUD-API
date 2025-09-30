from fastapi import FastAPI
from modules.users.routes import createUser

app = FastAPI()

# include router users
app.include_router(createUser.router)

@app.get("/")
def root():
    return {"msg": "Hello World"}

from fastapi import FastAPI

# items
from modules.items.routes import createItem, readItem, updateItem, deleteItem
# users
from modules.users.routes import createUser, readUser, updateUser, deleteUser

app = FastAPI()

# routers items
app.include_router(createItem.router)
app.include_router(readItem.router)
app.include_router(updateItem.router)
app.include_router(deleteItem.router)

# routers users
app.include_router(createUser.router)
app.include_router(readUser.router)
app.include_router(updateUser.router)
app.include_router(deleteUser.router)