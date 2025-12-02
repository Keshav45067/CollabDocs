
import logging
from typing import Optional
import grpc
from grpc import aio
from config.config import Config
from internal.repository.user import UserRepository
from proto.auth.v1 import auth_pb2
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User
from proto.common.v1 import common_pb2
from utils.hashing import verify_hash
from utils.jwt_token import JWT_handler

logger = logging.getLogger(__name__)
class LoginHandler():
    def __init__(self, session: AsyncSession):
        self.cnfg = Config()
        self.user_repo = UserRepository(session=session)

    async def _authenticate_user(self, email: str, password: str) -> Optional[User]:
        user: Optional[User] = await self.user_repo.get_user_with_email(email= email)
        if user is None:
            return None
        if not verify_hash(password, user.password):
            return None
        return user

    async def login(self, request: auth_pb2.LoginRequest, context : aio.ServicerContext)-> auth_pb2.LoginResponse:
        try:
            email = request.email.lower().strip()
            user: Optional[User] = await self._authenticate_user(email=email, password=request.password)
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
        except grpc.aio.AbortError:
            raise

        except Exception as err:
            logger.error(f"Internal Server Error: {err}")
            await context.abort(
                grpc.StatusCode.INTERNAL,
                f"Internal server error"
            )

