import logging
import os
import uuid

import cloudinary
import cloudinary.uploader
import dotenv
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session, joinedload

from database import get_db
from middleware.auth_middleware import getdata
from models.favorite import Favorite
from models.podcast_model import Podcast
from pydantic_schema.favorite import FavoritePodcast

logger = logging.getLogger(__name__)
dotenv.load_dotenv()

router = APIRouter()

# Cloudinary configuration
cloudinary.config( 
    cloud_name = "dcufgwk9h", 
    api_key = os.getenv("Api_key"), 
    api_secret = os.getenv("Api_Secret"),  # Ensure environment variables are properly loaded
    secure=True
)


# POST is more appropriate for uploading files
@router.post("/upload")
async def upload_podcast(
    podcastname: str = Form(...),
    author: str = Form(...),
    color: str = Form(...),
    thumbnail: UploadFile = File(...),
    audio: UploadFile = File(...),
    db: Session = Depends(get_db),
    user_id: dict = Depends(getdata)
):
    try:

        color = color.strip()
        if len(color) != 7 or not color.startswith("#"):
            raise HTTPException(status_code=400, detail="Invalid color format. Must be a HEX color code starting with '#'.")


        podcast_id = str(uuid.uuid4())
        

        audio_result = cloudinary.uploader.upload(
            audio.file,
            resource_type="auto",
            folder=f'podcasts/audio/{podcast_id}'
        )
        
       
        thumbnail_result = cloudinary.uploader.upload(
            thumbnail.file,
            resource_type="image",
            folder=f'podcasts/thumbnails/{podcast_id}'
        )
        
       
        new_podcast = Podcast(
            id=podcast_id,  # Assign the generated UUID
            color=color,
            podcast_name=podcastname,
            podcast_audio=audio_result['url'],
            author=author,
            thumbnail=thumbnail_result['url']
        )
        
        # Add new podcast to the database
        db.add(new_podcast)
        db.commit()
        db.refresh(new_podcast)

        return {"message": "Podcast uploaded successfully", "podcast": new_podcast}

    except Exception as e:
        logger.exception(f"Unexpected error in upload_podcast: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@router.get("/list")
def getpodcast( db: Session = Depends(get_db),
    user_id: dict = Depends(getdata)):
    podcast=db.query(Podcast).all()
    return podcast

@router.post('/favorite')
def favorite_podcast(podcast: FavoritePodcast, 
                     db: Session = Depends(get_db), 
                     auth_details = Depends(getdata)):
    user_id = auth_details['uid']
    
   
    fav_podcast = db.query(Favorite).filter(Favorite.podcast_id == podcast.podcast_id, Favorite.user_id == user_id).first()
    
    if fav_podcast:
        
        db.delete(fav_podcast)
        db.commit()
        return {'message': False}
    else:
       
        new_fav = Favorite(id=str(uuid.uuid4()), podcast_id=podcast.podcast_id, user_id=user_id)
        db.add(new_fav)
        db.commit()
        return {'message': True}

@router.get('/favorite/list')
def list_fav_podcasts(db: Session = Depends(get_db), 
                      auth_details = Depends(getdata)):
    user_id = auth_details['uid']
    
    
    fav_podcasts = db.query(Favorite).filter(Favorite.user_id == user_id).options(
        joinedload(Favorite.podcast)
    ).all()
    
 
    return fav_podcasts
    