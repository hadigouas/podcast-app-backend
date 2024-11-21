from sqlalchemy import TEXT, VARCHAR, Column, ForeignKey
from sqlalchemy.orm import relationship

from models.base import Base


class Favorite(Base):
    __tablename__ = "favorite"
    id = Column(TEXT, primary_key=True)
    podcast_id = Column(TEXT, ForeignKey("podcast.id"))
    user_id = Column(TEXT, ForeignKey("users.id"))
    
    podcast = relationship("Podcast", back_populates="favorite") 
    user = relationship("User", back_populates="favorite")        
