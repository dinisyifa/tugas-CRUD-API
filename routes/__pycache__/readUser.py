from fastapi import APIRouter, HTTPException, Query
from modules.users.schema.schemas import UserOut
from modules.users.routes.createUser import db

router = APIRouter()

# GET all users → hanya admin
@router.get("/users", response_model=list[UserOut])
def get_users(role: str = Query(...)):
    if role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can view all users")
    return list(db.values())

# GET single user → admin boleh semua, staff hanya user-nya sendiri
@router.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: str, role: str = Query(...)):
    if user_id not in db:
        raise HTTPException(status_code=404, detail="User not found")

    user = db[user_id]

    if role == "admin":
        return user

    if role == "staff":
        # staff hanya bisa lihat dirinya sendiri
        if user.role == "staff":
            return user
        raise HTTPException(status_code=403, detail="Staff cannot view other users")

    raise HTTPException(status_code=403, detail="Invalid role")