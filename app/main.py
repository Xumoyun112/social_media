from fastapi import FastAPI
# from sqladmin import Admin

from app.routers.users import router as user_router
from app.routers.auth import router as auth_router
from app.routers.post import router as post_router
from app.routers.post import app as post_app
from app.routers.like import router as like_router
from app.routers.comment import router as comment_router
from app.routers.follower import router as follower_router
from app.routers.chat import router as chat_router

# from .models import User, Post, Comment, Like, Follower
# from .database import engine

app = FastAPI()

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(post_router)
app.include_router(like_router)
app.include_router(comment_router)
app.include_router(post_app)
app.include_router(follower_router)
app.include_router(chat_router)

# admin = Admin(app=app, engine=engine, title="Admin Panel")

# admin.add_view(User)
# admin.add_view(Post)
# admin.add_view(Comment)
# admin.add_view(Like)
# admin.add_view(Follower)
