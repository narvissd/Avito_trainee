from fastapi import APIRouter, HTTPException, status
from app.schemas.users import UserUpdate, UserResponse
from app.models.users import Users

users_router = APIRouter()


@users_router.post("/users/setIsActive", response_model=UserResponse)
async def set_is_active(data: UserUpdate):
    updated_user = await Users.set_is_active(data.user_id, data.is_active)

    if updated_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"code": "NOT_FOUND", "message": "User not found"}}
        )
    return {"user": updated_user}
