
from fastapi import APIRouter, HTTPException, status
from datetime import datetime
import uuid
from modules.users.schema.schemas import UserCreate, UserOut, UserInDB

router = APIRouter()
db: dict = {}

@router.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    for existing in db.values():
        if existing.email == user.email:
            raise HTTPException(status_code=400, detail="Email already exists")
        if existing.username == user.username:
            raise HTTPException(status_code=400, detail="Username already exists")

    user_id = uuid.uuid4()
    now = datetime.utcnow()
    new_user = UserInDB(
        id=user_id,
        username=user.username,
        email=user.email,
        role=user.role,
        created_at=now,
        updated_at=now,
        password=user.password  # simpan plain dulu (atau hash kalau mau)
    )
    db[str(user_id)] = new_user
    return new_user