from sqlalchemy import TEXT, VARCHAR, Column
from sqlalchemy.orm import relationship

from models.base import Base


class Podcast(Base):
    __tablename__="podcast"
    id=Column(TEXT,primary_key=True)
    author=Column(VARCHAR(255))
    thumbnail=Column(TEXT)
    podcast_audio=Column(TEXT)
    podcast_name=Column(TEXT)
    color=Column(VARCHAR(7))
    favorite = relationship("Favorite", back_populates="podcast")