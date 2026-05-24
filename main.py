from fastapi import FastAPI
from artists.router import router as artists_router

app = FastAPI(title="Music Library API")

app.include_router(artists_router)

@app.get("/")
def root():
    return {"message": "Music Library API"}