from pydantic import BaseModel


class FavoritePodcast(BaseModel):
    podcast_id: str