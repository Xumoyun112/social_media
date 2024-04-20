from fastapi import Depends, APIRouter, HTTPException
from starlette import status
from app.services.oauth2 import get_current_user
from app.database import get_db

router = APIRouter(prefix="/follower", tags=['follower'])


@router.post("/", status_code=status.HTTP_201_CREATED)
def follow_to_user(db=Depends(get_db), user=Depends(get_current_user)):
    pass
