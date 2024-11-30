from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.contact import ContactCreate, ContactUpdate
from src.repository.contacts import ContactRepository

class ContactService:
    def __init__(self, db: AsyncSession):
        self.repository = ContactRepository(db)

    async def get_contacts(self, skip: int, limit: int):
        return await self.repository.get_all(skip, limit)

    async def get_contact(self, contact_id: int):
        return await self.repository.get_by_id(contact_id)

    async def create_contact(self, body: ContactCreate):
        return await self.repository.create(body)

    async def update_contact(self, contact_id: int, body: ContactUpdate):
        return await self.repository.update(contact_id, body)

    async def delete_contact(self, contact_id: int):
        return await self.repository.delete(contact_id)

    async def search_contacts(self, query: str, skip: int, limit: int):
        return await self.repository.search_contacts(query, skip, limit)

    async def get_upcoming_birthdays(self):
        return await self.repository.get_upcoming_birthdays()