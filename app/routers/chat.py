from fastapi import APIRouter, Depends, HTTPException, WebSocket

from app.database import get_db
from app.models import User, Room, Message
from app.services.oauth2 import get_current_user, verify_access_token
from starlette import status
from app.schemas import RoomCreate, RoomOutput
from sqlalchemy import or_

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=RoomOutput)
def create_room(room: RoomCreate, db=Depends(get_db), current_user=Depends(get_current_user)):
    new_room = Room(name=room.name)
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room


@router.post("/room-create-private", status_code=status.HTTP_201_CREATED, response_model=RoomOutput)
def create_room_private(user_id: int, db=Depends(get_db), current_user: User = Depends(get_current_user)):
    room = db.query(Room).filter(or_(Room.name == f"{user_id}_{current_user.id}",
                                     Room.name == f"{current_user.id}_{user_id}")).first()
    if room:
        return room
    new_room = Room(name=f"{user_id}_{current_user.id}")
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room


@router.get("/room-list", status_code=status.HTTP_200_OK)
def get_rooms(db=Depends(get_db)):
    return db.query(Room).all()


@router.websocket("/room/{room_id}")
async def create_message(room_id: int, websocket: WebSocket,
                         db=Depends(get_db)):
    await websocket.accept()
    token = websocket.headers['Authorization'].split(' ')[1]
    user_id = verify_access_token(token)
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        await websocket.close()
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not Found")
    try:
        while True:
            data = await websocket.receive_text()
            message = Message(room_id=room_id, owner_id=user_id, content=data)
            print(message.content)
            db.add(message)
            db.commit()
            db.refresh(message)
            await websocket.send_text(f"Message received: {data}")
    except:
        await websocket.close()
