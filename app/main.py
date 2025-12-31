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
async def get_contacts():
    contacts = get_all_contacts()
    return contacts


@app.post("/contacts/")
async def add_contact(contact: ContactCreate):
    dict_contact = contact.model_dump()
    new_id = create_contact(dict_contact)
    if not new_id:
        raise HTTPException(status_code=401, detail="Phone number already exist")
    return {"message": "Contact created successfully", "id": new_id}


@app.put("/contacts/{contact_id}")
async def update_contact_api(contact_id, data: ContactUpdate):
    dict_contact = data.model_dump()
    updated = update_contact(contact_id, dict_contact)

    if updated == "not_uniqe":
        raise HTTPException(status_code=401, detail="Phone number already exist")
    
    if not updated:
        raise HTTPException(status_code=404, detail="Contact not found")

    return {"message": "Update was successful"}


@app.delete("/contacts/{contact_id}")
async def delete_contact_api(contact_id: int):
    success = delete_contact(contact_id)
    if not success:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"message": "Contact deleted successfully"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

