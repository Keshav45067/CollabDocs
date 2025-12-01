from typing import Optional, Tuple
import grpc
import bcrypt
from sqlalchemy import Result, select
from config.config import Config
from proto.auth.v1 import auth_pb2
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User
from proto.common.v1 import common_pb2
from utils.jwt_token import JWT_handler

class LoginHandler():
    def __init__(self, session: AsyncSession):
        self.session = session
        self.cnfg = Config()

    @staticmethod
    def _verify_password(raw_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(raw_password.encode(), hashed_password.encode())


    async def _authenticate_user(self, email: str, password: str) -> Optional[User]:
        stmt = select(User).where(User.email == email)
        result: Result[Tuple[User]] = await self.session.execute(stmt)
        user: Optional[User] = result.scalar_one_or_none()
        if user is None:
            return None
        if not self._verify_password(password, user.password):
            return None

        return user

    async def login(self, request: auth_pb2.LoginRequest, context : grpc.ServicerContext)-> auth_pb2.LoginResponse:
        try:
            user: Optional[User] = await self._authenticate_user(email=request.email, password=request.password)
            if user is None:
                await context.abort(
                    grpc.StatusCode.UNAUTHENTICATED,
                    "Invalid Credentials"
                )
            jwt_handler = JWT_handler(
                private_key_pem=self.cnfg.jwt_private_key,
                public_key_pem=self.cnfg.jwt_public_key
                )
            token = jwt_handler.create_access_token(subject=str(user.id))

            return auth_pb2.LoginResponse(
                success=True,
                user_id = common_pb2.Uuid(value=str(user.id)),
                token= token
            )
        except Exception as err:
            await context.abort(
                grpc.StatusCode.INTERNAL,
                f"Internal server error"
            )

