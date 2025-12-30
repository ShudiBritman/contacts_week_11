from data_interactor import *
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn


class ContactCreate(BaseModel):
    first_name: str
    last_name: str
    phone_number: str

class ContactUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None

app = FastAPI()


@app.get("/contacts/")
def get_contacts():
    contacts = get_all_contacts()
    return contacts


@app.post("/contacts/")
def add_contact(contact: ContactCreate):
    new_id = create_contact(
        contact.first_name,
        contact.last_name,
        contact.phone_number
    )
    return {"message": "Contact created successfully", "id": new_id}


@app.put("/contacts/{contact_id}")
def update_contact_api(contact_id: int, data: ContactUpdate):
    updated = update_contact(
        contact_id,
        data.first_name,
        data.last_name,
        data.phone_number
    )

    if not updated:
        raise HTTPException(status_code=404, detail="Contact not found")

    return {"message": "Update was successful"}


@app.delete("/contacts/{contact_id}")
def delete_contact_api(contact_id: int):
    success = delete_contact(contact_id)
    if not success:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"message": "Contact deleted successfully"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

