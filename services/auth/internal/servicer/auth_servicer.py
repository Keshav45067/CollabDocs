import logging
import grpc
from internal.controller.login import LoginHandler
from internal.controller.register import RegisterHandler
from proto.auth.v1.auth_pb2 import LoginRequest, LoginResponse, RegisterRequest, RegisterResponse, ResendOtpRequest, ResendOtpResponse, VerifyOtpRequest, VerifyOtpResponse
from proto.auth.v1.auth_pb2_grpc import AuthServiceServicer
from config.db import SessionFactory

logger = logging.getLogger(__name__)
class AuthServicer(AuthServiceServicer):

    async def Login(self, request : LoginRequest, context : grpc.aio.ServicerContext) -> LoginResponse:
        async with SessionFactory() as session:
            login_handler: LoginHandler = LoginHandler(session=session)
            res: LoginResponse = await login_handler.login(request=request, context=context)
            await session.commit()
        logger.info("Auth done")
        return res

    async def Register(self, request: RegisterRequest, context: grpc.aio.ServicerContext)-> RegisterResponse:
        async with SessionFactory() as session:
            register_handler: RegisterHandler = RegisterHandler(session=session)
            res: RegisterResponse = await register_handler.register(request=request, context=context)
            await session.commit()
        return res 

    async def ResendOtp(self, request: ResendOtpRequest, context: grpc.aio.ServicerContext)-> ResendOtpResponse:
        async with SessionFactory() as session:
            register_handler: RegisterHandler = RegisterHandler(session=session)
            res: ResendOtpResponse = await register_handler.resend_otp(request=request, context=context)
            await session.commit()
        return res

    async def VerifyOtp(self, request: VerifyOtpRequest, context: grpc.aio.ServicerContext)-> VerifyOtpResponse:
        async with SessionFactory() as session:
            register_handler: RegisterHandler = RegisterHandler(session=session)
            res: VerifyOtpResponse = await register_handler.verify_otp(request=request, context=context)
            await session.commit()
        return res
        

                
        


