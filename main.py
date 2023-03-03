from fastapi import FastAPI
from . import models
from .database import engine
from .routers import blog, User, auth
app = FastAPI()
app.include_router(blog.router)
app.include_router(User.router)
app.include_router(auth.router)
models.Base.metadata.create_all(bind=engine)

