import asyncio
from config.config import Config
import grpc
import logging
from internal.servicer.auth_servicer import AuthServicer
from proto.auth.v1 import auth_pb2_grpc

logger  = logging.getLogger(__name__)
class AuthServer():

    def __init__(self, config: Config):
        self.config = config
        self._server: grpc.aio.Server | None = None

    def _build_server(self, auth_servicer: AuthServicer, server_credentials: grpc.ServerCredentials | None = None)-> grpc.aio.Server:
        server = grpc.aio.server()
        auth_pb2_grpc.add_AuthServiceServicer_to_server(servicer = auth_servicer, server=server)
        if self.config.is_production:
            assert server_credentials is not None, "Server Credentials are not provided"
            server.add_secure_port(self.config.address(), server_credentials=server_credentials)
        else:
            
            server.add_insecure_port(self.config.address())
        
        return server

    async def start(self, server_credentials: grpc.ServerCredentials | None = None):
        logging.info(f"Starting Server on address: {self.config.address()}")
        self._server = self._build_server(auth_servicer=AuthServicer(), server_credentials=server_credentials)
        await self._server.start()
        logger.info("Auth gRPC server started")

    async def stop(self, grace: float = 10.0) -> None:
        assert self._server is not None, "Server not started"
        logger.info("Stopping Auth gRPC server gracefully...")
        await self._server.stop(grace=grace)
        logger.info("Auth gRPC server stopped")

