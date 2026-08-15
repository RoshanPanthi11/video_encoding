from fastapi import FastAPI

from app.database import Base, engine
from app.models.video import EncodingJob
from app.routers.video import router as video_router


Base.metadata.create_all(bind=engine)


app = FastAPI(title="Video Encoding API")

app.include_router(video_router)


@app.get("/")
def home():
    return {
        "message": "Video Encoding API is running"
    }