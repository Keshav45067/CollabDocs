import logging
import grpc
from proto.auth.v1 import auth_pb2, auth_pb2_grpc
from proto.common.v1 import common_pb2

logger = logging.getLogger(__name__)
class AuthServicer(auth_pb2_grpc.AuthServiceServicer):

    def Login(self, request : auth_pb2.LoginRequest, context : grpc.ServicerContext) -> auth_pb2.LoginResponse:
        logger.info("Request recieved with email:", request.email)
        print("Request recieved with email:", request.email)
        uuid = common_pb2.Uuid()
        response: auth_pb2.LoginResponse = auth_pb2.LoginResponse(
            success=True,
            user_id=uuid,
            error=None
        )
        return response


