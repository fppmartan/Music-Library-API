from fastapi import FastAPI
from artists.router import router as artists_router
from albums.router import router as albums_router
from songs.router import router as songs_router

app = FastAPI(title="Music Library API")

app.include_router(artists_router)
app.include_router(albums_router)
app.include_router(songs_router)

@app.get("/")
def root():
    return {"message": "Music Library API"}