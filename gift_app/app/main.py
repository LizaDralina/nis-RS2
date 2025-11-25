from typing import Dict

from fastapi import FastAPI

from app.api.recipients import router as recipients_router

app = FastAPI(
    title="Gift Helper API",
    description="Минимальный прототип для управления получателями подарков",
    version="1.0.0",
)

app.include_router(recipients_router)


@app.get("/")
def read_root() -> Dict[str, str]:
    return {"message": "Gift Helper API"}


@app.get("/health")
def health_check() -> Dict[str, str]:
    return {"status": "healthy"}
