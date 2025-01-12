from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

from typing import Optional

from .models import Base, User


class Database:
    def __init__(self):
        self.engine = create_async_engine(
            "sqlite+aiosqlite:///src/data/database/database_file/database.sqlite",
            echo=False
        )
        self.async_session = sessionmaker(
            self.engine, 
            class_=AsyncSession, 
            expire_on_commit=False
        )

    async def init_db(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def create_user(self, _id: int, initial_balance: float = 0.0) -> Optional[User]:
        async with self.async_session() as session:
            query = select(User).where(User.id == _id)
            result = await session.execute(query)
            existing_user = result.scalar_one_or_none()
            
            if not existing_user:
                user = User(id=_id, balance=initial_balance)
                session.add(user)
                await session.commit()

    async def update_balance(self, _id: int, new_balance: float) -> Optional[User]:
        async with self.async_session() as session:
            query = select(User).where(User.id == _id)
            result = await session.execute(query)
            user = result.scalar_one_or_none()
            
            if user:
                user.balance = new_balance
                await session.commit()
                return user
            return None