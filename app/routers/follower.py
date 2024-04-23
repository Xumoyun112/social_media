from fastapi import Depends, APIRouter, HTTPException
from starlette import status
from app.services.oauth2 import get_current_user
from app.database import get_db
from app.models import User, Follower
from app.schemas import AllFollowingShema, AllFollowerShema
from sqlalchemy import or_

router = APIRouter(prefix="/follower", tags=['follower'])


@router.post("/{user_id}", status_code=status.HTTP_201_CREATED)
def follow_to_user(user_id: int, db=Depends(get_db), current_user=Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not Found")
    if user_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can't follow yourself")
    follower = Follower(following_id=current_user.id, follower_id=user.id)
    db.add(follower)
    db.commit()
    db.refresh(follower)
    return {"Message": "Follower added"}


@router.post("/is_following/{user_id}", status_code=status.HTTP_201_CREATED)
def is_following(user_id: int, db=Depends(get_db), current_user=Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not Found")
    follower = db.query(Follower).filter(Follower.following_id == user.id, Follower.follower_id == current_user.id)
    if not follower.first():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can't follow user")
    follower.update({"is_following": True})
    db.commit()
    return {"message": "User followed"}


@router.delete("/delete/{user_id}")
def delete_follower(user_id: int, db=Depends(get_db), current_user=Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not Found")
    follower = db.query(Follower).filter(Follower.following_id == user.id, Follower.follower_id == current_user.id)
    if not follower.first():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can't follow user")
    follower.delete()
    db.commit()
    return {"message": "User deleted"}


@router.get("/followers", response_model=list[AllFollowerShema])
def all_follower(db=Depends(get_db), current_user=Depends(get_current_user)):
    follower = db.query(Follower).filter(Follower.following_id == current_user.id)
    return follower


@router.get("/followings", response_model=list[AllFollowingShema])
def all_following(db=Depends(get_db), current_user=Depends(get_current_user)):
    following = db.query(Follower).filter(Follower.follower_id == current_user.id)
    return following
