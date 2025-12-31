from connection import Singelton, Connector

client = Singelton.get_connection_to_mongo()

def get_collection():
    contacts_db = Connector.get_database(client)
    contacts = Connector.get_collection(contacts_db)
    return contacts


def get_all_contacts():
    col_contacts = get_collection()
    contacts = col_contacts.find()
    for contact in contacts:
        contact["_id"] = str(contact["_id"]) 
        yield contact
    return contacts
    


def create_contact(contact_data):
    col_contacts = get_collection()
    insert_contacts = col_contacts.insert_one(contact_data)
    result = col_contacts.find_one({"phone_number": contact_data["phone_number"]})
    return str(result["_id"])



def update_contact(contcat_id: str, contact_data: dict):
    col_contacts = get_collection()
    doc = {}
    for k, v in contact_data.items():
        if v:
            doc.update({k: v})
    result = col_contacts.update_one(
        {"id": contcat_id},
        {"$set":doc}
    )
    return


def delete_contact(contact_id: str):
    col_contacts = get_collection()
    result = col_contacts.delete_one({'id':contact_id})
    return True


