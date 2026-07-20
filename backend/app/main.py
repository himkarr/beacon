from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.repository.api import router as repository_router

app = FastAPI(
    title="Beacon",
    version="1.0.0",
    description="AI Powered Application Security Platform"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(repository_router)


@app.get("/")
async def root():
    return {"message": "Beacon Backend Running"}