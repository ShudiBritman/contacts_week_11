from connection import Singelton, Connector
from models import Contact
from bson import ObjectId

client = Singelton.get_connection_to_mongo()

def get_collection():
    contacts_db = Connector.get_database(client)
    contacts = Connector.get_collection(contacts_db)
    return contacts


def get_all_contacts():
    col_contacts = get_collection()
    contacts = col_contacts.find()
    object_contacts = []
    for contact in contacts:
        object_contact = Contact.from_mongo(contact) 
        object_contacts.append(object_contact.to_dict())
    return object_contacts
    


def create_contact(contact_data: dict):
    col_contacts = get_collection()
    uniqe_valid = unique_num_phone_valid(contact_data["phone_number"])
    if not uniqe_valid:
        return False
    object_contact = Contact.to_mongo(contact_data)
    insert_contacts = col_contacts.insert_one(object_contact.to_dict())
    result = col_contacts.find_one({"phone_number": contact_data["phone_number"]})
    return str(result["_id"])



def update_contact(contcat_id: str, contact_data: dict):
    col_contacts = get_collection()
    doc = {k: v for k, v in contact_data.items() if not v is None}
    if "phone_number" in doc:
        uniqe_valid = unique_num_phone_valid(doc["phone_number"])
        if not uniqe_valid:
            return "not_uniqe"
    result = col_contacts.update_one(
        {"_id": ObjectId(contcat_id)},
        {"$set":doc}
    )
    return result

def delete_contact(contact_id: str):
    col_contacts = get_collection()
    result = col_contacts.delete_one({'_id' :ObjectId(contact_id)})
    return result



def unique_num_phone_valid(phone_number):
    col_contacts = get_collection()
    result = col_contacts.count_documents({"phone_number": phone_number})
    if result > 0:
        return False
    return True