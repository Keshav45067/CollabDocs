import logging
import grpc
from proto.auth.v1.auth_pb2 import LoginRequest, LoginResponse
from proto.auth.v1.auth_pb2_grpc import AuthServiceServicer
from proto.common.v1 import common_pb2

logger = logging.getLogger(__name__)
class AuthServicer(AuthServiceServicer):

    def Login(self, request : LoginRequest, context : grpc.ServicerContext) -> LoginResponse:
        logger.info(f"Request recieved with email: {request.email}")

        # Dummy Code
        uuid = common_pb2.Uuid()
        response: LoginResponse = LoginResponse(
            success=True,
            user_id=uuid,
            error=None
        )
        return response


