import asyncio
from datetime import datetime, timedelta, timezone
from random import randint
from typing import Optional
import grpc
from sqlalchemy.ext.asyncio import AsyncSession
from internal.repository.email_verification import EmailVerificationRepository
from internal.repository.user import UserRepository
from models.email_verification import EmailVerification
from models.user import User
from proto.auth.v1 import auth_pb2
from utils.hashing import create_hash, verify_hash
import logging

from utils.regex import is_valid_email, is_valid_password

logger = logging.getLogger(__name__)
class RegisterHandler():
    def __init__(self, session: AsyncSession):
        self.user_repo = UserRepository(session=session)
        self.email_verf_repo = EmailVerificationRepository(session=session)

    @staticmethod
    async def send_mail(otp: int, email: str):
        logger.info(f"Email: {email}, OTP: {otp}")

    def _success_response_register(self, otp: int, email: str)-> auth_pb2.RegisterResponse:
        asyncio.create_task(self.send_mail(otp=otp, email=email))
        return auth_pb2.RegisterResponse(success=True, error="", time=0)

    def _can_resend_otp(self, email_verf_result: Optional[EmailVerification])-> tuple[bool, float]:
        assert email_verf_result is not None, "Email verification object is None, at Register RPC"

        time_now = datetime.now(timezone.utc)
        time_left: timedelta = email_verf_result.next_resend_at - time_now 

        time_left_seconds: float = 0.0
        ok: bool = True

        if(time_left > timedelta(0)):
            time_left_seconds = time_left.total_seconds()
            ok = False

        return ok, time_left_seconds

    def _is_otp_valid(self, email_verf_result: Optional[EmailVerification], otp: str)-> tuple[bool, str]:
        assert email_verf_result is not None, "Email verification object is None, at Register RPC"

        time_now = datetime.now(timezone.utc)
        ok: bool = verify_hash(otp, email_verf_result.otp_hash)

        if time_now > email_verf_result.otp_expires_at:
            return False, "otp expired"
        if not ok:
            return False, "wrong otp"
        
        return True, ""
        

    async def register(self, request: auth_pb2.RegisterRequest, context: grpc.aio.ServicerContext)-> auth_pb2.RegisterResponse:
        try:
            email = request.email.lower().strip()
            user: Optional[User] = await self.user_repo.get_user_with_email(email= email)
            if user is not None:
                await context.abort(
                    grpc.StatusCode.ALREADY_EXISTS,
                    "User with provided email already exists"
                )
            if not is_valid_email(email=email):
                await context.abort(
                    grpc.StatusCode.INVALID_ARGUMENT,
                    "Invalid Email"
                )

            if not is_valid_password(password=request.password):
                await context.abort(
                    grpc.StatusCode.INVALID_ARGUMENT,
                    "Invalid Password"
                )

            email_verf_result: Optional[EmailVerification] = await self.email_verf_repo.get_email_verification(email= email)

            otp: int = randint(1000, 9999)
            hashed_otp: str = create_hash(str(otp))
            hashed_password: str = create_hash(str(request.password))
            if email_verf_result is None:
                self.email_verf_repo.create_email_verfification(
                    email= email, 
                    name= request.name,
                    otp_hash= hashed_otp,
                    password_hash= hashed_password,
                )
                return self._success_response_register(otp= otp, email= email)

            ok, time_left = self._can_resend_otp(email_verf_result= email_verf_result)
            if not ok:
                return auth_pb2.RegisterResponse(
                    success= False,
                    error= "OTP resend cooldown is still going on",
                    time= int(time_left)
                )

            self.email_verf_repo.update_email_verification(
                email_verf= email_verf_result,
                otp_hash= hashed_otp, 
            )
            return self._success_response_register(otp= otp, email= email)

        except grpc.aio.AbortError:
            raise
        except Exception as err:
            logger.error(f"Internal Server Error: {err}")
            await context.abort(
                grpc.StatusCode.INTERNAL,
                f"Internal server error"
            )

    async def resend_otp(self, request: auth_pb2.ResendOtpRequest, context: grpc.aio.ServicerContext)-> auth_pb2.ResendOtpResponse:
        try:
            email = request.email.lower().strip()
            user: Optional[User] = await self.user_repo.get_user_with_email(email= email)
            if user is not None:
                await context.abort(
                    grpc.StatusCode.ALREADY_EXISTS,
                    "User with provided email already exists"
                )

            email_verf_result: Optional[EmailVerification] = await self.email_verf_repo.get_email_verification(email= email)

            if email_verf_result is None:
                await context.abort(
                    grpc.StatusCode.INVALID_ARGUMENT,
                    "OTP was never sent"
                )
            
            ok, time_left = self._can_resend_otp(email_verf_result= email_verf_result)
            if not ok:
                return auth_pb2.ResendOtpResponse(
                    success= False,
                    time= int(time_left)
                )

            otp: int = randint(1000, 9999)
            hashed_otp: str = create_hash(str(otp))

            self.email_verf_repo.update_email_verification(
                email_verf=email_verf_result,
                otp_hash= hashed_otp, 
            )
            return self._success_response_register(otp= otp, email= email)
        except grpc.aio.AbortError:
            raise
        except Exception as err:
            logger.error(f"Internal Server Error: {err}")
            await context.abort(
                grpc.StatusCode.INTERNAL,
                "Internal Server Error"
            )

    async def verify_otp(self, request: auth_pb2.VerifyOtpRequest, context: grpc.aio.ServicerContext)-> auth_pb2.VerifyOtpResponse:
        try:
            email = request.email.lower().strip()
            user: Optional[User] = await self.user_repo.get_user_with_email(email= email)
            if user is not None:
                await context.abort(
                    grpc.StatusCode.ALREADY_EXISTS,
                    "User with provided email already exists"
                )

            email_verf_result: Optional[EmailVerification] = await self.email_verf_repo.get_email_verification(email= email)
            if email_verf_result is None:
                await context.abort(
                    grpc.StatusCode.INVALID_ARGUMENT,
                    "Email not found"
                ) 
            ok, message = self._is_otp_valid(email_verf_result=email_verf_result, otp = request.otp)
            if not ok:
                await context.abort(grpc.StatusCode.UNAUTHENTICATED, message)

            self.user_repo.create_user(
                email = email_verf_result.email,
                password = email_verf_result.password_hash,
                name= email_verf_result.name
            )
            await self.email_verf_repo.delete_email_verification(email_verf=email_verf_result)

            return auth_pb2.VerifyOtpResponse(
                success= True
            )

        except grpc.aio.AbortError:
            raise
        except Exception as err:
            logger.error(f"Internal Server error: {err}")
            await context.abort(
                grpc.StatusCode.INTERNAL,
                "Internal server error"
            )
        




        

            

        

