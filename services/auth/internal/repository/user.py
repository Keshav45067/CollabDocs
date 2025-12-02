
from typing import Optional, Tuple
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession


from models.user import User

class UserRepository():
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_with_email(self, email: str)-> Optional[User]:
        stmt = select(User).where(User.email == email)
        result: Result[Tuple[User]] = await self.session.execute(stmt)
        user: Optional[User] = result.scalar_one_or_none
        return user

    def create_user(self, email: str, password: str, name: str)-> User:
        user = User(
            name= name,
            email= email,
            password= password
        )
        self.session.add(user)
        return user
    


