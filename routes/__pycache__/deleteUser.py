from fastapi import APIRouter, HTTPException, Query
from modules.users.routes.createUser import db

router = APIRouter()

@router.delete("/users/{user_id}")
def delete_user(user_id: str, role: str = Query(...)):
    if role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can delete users")
    if user_id not in db:
        raise HTTPException(status_code=404, detail="User not found")
    deleted = db.pop(user_id)
    return {"message": "User deleted successfully", "data": deleted}