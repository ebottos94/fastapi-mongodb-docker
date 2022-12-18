from fastapi import FastAPI
from .routes import router as AppRouter


app = FastAPI()

app.include_router(AppRouter, tags=["Api"], prefix="/api/v1")
