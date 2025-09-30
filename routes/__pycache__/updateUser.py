from fastapi import APIRouter, HTTPException, Query
from datetime import datetime
from modules.users.schema.schemas import UserCreate, UserOut, UserInDB
from modules.users.routes.createUser import db

router = APIRouter()

@router.put("/users/{user_id}", response_model=UserOut)
def update_user(user_id: str, new_data: UserCreate, role: str = Query(...)):
    if role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can update users")
    if user_id not in db:
        raise HTTPException(status_code=404, detail="User not found")

    existing_user = db[user_id]

    # buat user baru dengan data update
    updated_user = UserInDB(
        id=existing_user.id,
        username=new_data.username,
        email=new_data.email,
        role=new_data.role,
        password=new_data.password,  # simpan password baru (plain/hashing opsional)
        created_at=existing_user.created_at,
        updated_at=datetime.utcnow()
    )

    db[user_id] = updated_user
    return updated_user