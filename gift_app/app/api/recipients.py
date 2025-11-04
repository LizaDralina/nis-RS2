
from fastapi import APIRouter, HTTPException
from app.models import schemas
from app.services.recipient_service import RecipientService
from app.repositories.recipient_repo import InMemoryRecipientRepository

repo = InMemoryRecipientRepository()
service = RecipientService(repo)

router = APIRouter(prefix="/recipients", tags=["recipients"])

@router.post("/", response_model=schemas.RecipientRead)
def create_recipient(recipient_in: schemas.RecipientCreate):
    recipient = service.create_recipient(
        name=recipient_in.name,
        relation=recipient_in.relation,
        age=recipient_in.age,
    )
    return schemas.RecipientRead(**recipient.__dict__)

@router.get("/{recipient_id}", response_model=schemas.RecipientRead)
def get_recipient(recipient_id: int):
    recipient = service.get_recipient(recipient_id)
    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient not found")
    return schemas.RecipientRead(**recipient.__dict__)

@router.get("/", response_model=list[schemas.RecipientRead])
def get_all_recipients():
    recipients = service.get_all_recipients()
    return [schemas.RecipientRead(**recipient.__dict__) for recipient in recipients]