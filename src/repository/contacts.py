from datetime import date, timedelta
from typing import List, Optional

from sqlalchemy import select, or_, and_, extract
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Contact
from src.schemas.contact import ContactCreate, ContactUpdate


class ContactRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self, skip: int = 0, limit: int = 100, user_id: int = None) -> List[Contact]:
        stmt = select(Contact).filter_by(user_id=user_id).offset(skip).limit(limit)
        contacts = await self.session.execute(stmt)
        return contacts.scalars().all()

    async def get_by_id(self, contact_id: int, user_id: int) -> Optional[Contact]:
        stmt = select(Contact).filter_by(id=contact_id, user_id=user_id)
        contact = await self.session.execute(stmt)
        return contact.scalar_one_or_none()

    async def create(self, body: ContactCreate, user_id: int) -> Contact:
        contact_data = body.model_dump()
        contact_data['user_id'] = user_id
        contact = Contact(**contact_data)
        self.session.add(contact)
        await self.session.commit()
        await self.session.refresh(contact)
        return contact

    async def update(self, contact_id: int, body: ContactUpdate, user_id: int) -> Optional[Contact]:
        stmt = select(Contact).filter_by(id=contact_id, user_id=user_id)
        result = await self.session.execute(stmt)
        contact = result.scalar_one_or_none()

        if contact:
            for key, value in body.model_dump(exclude_unset=True).items():
                setattr(contact, key, value)
            await self.session.commit()
            await self.session.refresh(contact)

        return contact

    async def delete(self, contact_id: int, user_id: int) -> Optional[Contact]:
        stmt = select(Contact).filter_by(id=contact_id, user_id=user_id)
        contact = await self.session.execute(stmt)
        contact = contact.scalar_one_or_none()

        if contact:
            await self.session.delete(contact)
            await self.session.commit()

        return contact

    async def search_contacts(
            self,
            search_query: str,
            skip: int = 0,
            limit: int = 10,
            user_id: int = None
    ) -> List[Contact]:
        search = f"%{search_query}%"
        stmt = select(Contact).filter(
            and_(
                or_(
                    Contact.first_name.ilike(search),
                    Contact.last_name.ilike(search),
                    Contact.email.ilike(search)
                ),
                Contact.user_id == user_id
            )
        ).offset(skip).limit(limit)

        contacts = await self.session.execute(stmt)
        return contacts.scalars().all()

    async def get_upcoming_birthdays(self, user_id: int) -> List[Contact]:
        today = date.today()
        seven_days_later = today + timedelta(days=7)

        stmt = select(Contact).filter(
            and_(
                or_(
                    and_(
                        extract('month', Contact.birth_date) == today.month,
                        extract('day', Contact.birth_date) >= today.day,
                        extract('day', Contact.birth_date) <= seven_days_later.day
                    ),
                    and_(
                        extract('month', Contact.birth_date) == seven_days_later.month,
                        extract('day', Contact.birth_date) <= seven_days_later.day
                    )
                ),
                Contact.user_id == user_id
            )
        )
        contacts = await self.session.execute(stmt)
        return contacts.scalars().all()