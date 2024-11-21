import uuid

import bcrypt
from fastapi import FastAPI, HTTPException

from database import engine
from models.base import Base
from routes import auth_rout, podcast_rout

app = FastAPI()
app.include_router(auth_rout.router, prefix="/auth")
app.include_router(podcast_rout.router,prefix="/podcast")
Base.metadata.create_all(engine)


