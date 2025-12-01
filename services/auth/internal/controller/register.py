import asyncio
from datetime import datetime, timezone
from random import randint
from typing import Optional
import grpc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import session

from models.email_verification import EmailVerification
from models.user import User
from proto.auth.v1 import auth_pb2


class RegisterHandler():
    def __init__(self, session: AsyncSession):
        self.session = session

    def _success_response_register(self, otp: int, email: str)-> auth_pb2.RegisterResponse:
        asyncio.create_task(send_mail(otp=otp, email=email))
        return auth_pb2.RegisterResponse(success=True, error="", time=0)

    async def register(self, request: auth_pb2.RegisterRequest, context: grpc.ServicerContext):
        user: Optional[User] = await get_user_with_email(email= request.email, session= session)
        if user is not None:
            await context.abort(
                grpc.StatusCode.ALREADY_EXISTS,
                "User with provided email already exists"
            )
        
        email_verf_result: Optional[EmailVerification] = await get_email_verification(email= request.email)

        otp: int = randint(1000, 9999)
        hashed_otp: str = create_hash(str(otp))

        if email_verf_result is None:
            create_email_verfification(
                email= request.email, 
                hashed_otp= hashed_otp, 
                session= session
            )
            return self._success_response_register(otp= otp, email= request.email)

        ok, time_left = _can_resend_otp(email_verf_result: email_verf_result)
        if not ok:
            return auth_pb2.RegisterResponse(
                success= False,
                error= "OTP resend cooldown is still going on",
                time= int(time_left)
            )

        await update_email_verification(
            email= request.email, 
            hashed_otp= hashed_otp, 
            session= session
        )
        return self._success_response_register(otp= otp, email= request.email)

    async def resend_otp(self, request: auth_pb2.RegisterRequest, context: grpc.ServicerContext):
        user: Optional[User] = await get_user_with_email(email= request.email, session= session)
        if user is not None:
            await context.abort(
                grpc.StatusCode.ALREADY_EXISTS,
                "User with provided email already exists"
            )

        email_verf_result: Optional[EmailVerification] = await get_email_verification(email= request.email)

        if email_verf_result is None:
            await context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "OTP was never sent"
            )
        
        ok, time_left = _can_resend_otp(email_verf_result: email_verf_result)
        if not ok:
            return auth_pb2.RegisterResponse(
                success= False,
                error= "OTP resend cooldown is still going on",
                time= int(time_left)
            )
            
        otp: int = randint(1000, 9999)
        hashed_otp: str = create_hash(str(otp))

        await update_email_verification(
            email= request.email, 
            hashed_otp= hashed_otp, 
            session= session
        )
        return self._success_response_register(otp= otp, email= request.email)

        




        

            

        

