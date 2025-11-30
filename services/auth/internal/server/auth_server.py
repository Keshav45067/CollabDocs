from concurrent import futures
from config.config import Config
import grpc
import logging
from internal.servicer.auth_servicer import AuthServicer
from proto.auth.v1 import auth_pb2_grpc

logger  = logging.getLogger(__name__)
class AuthServer():

    def __init__(self, config: Config):
        self.config = config
        self._server: grpc.Server | None = None

    def _build_server(self, auth_servicer: auth_pb2_grpc.AuthServiceServicer, server_credentials: grpc.ServerCredentials | None = None)-> grpc.Server:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        auth_pb2_grpc.add_AuthServiceServicer_to_server(servicer = auth_servicer, server=server)
        if self.config.is_production:
            # if server_credentials is None:
            #     Throw new error
            server.add_secure_port(self.config.address(), server_credentials=server_credentials)
        else:
            
            server.add_insecure_port(self.config.address())
        
        return server

    def start(self, server_credentials: grpc.ServerCredentials | None = None):
        logging.info("Starting Server on address: ", self.config.address())
        print("Starting Server on address: ", self.config.address())
        self._server = self._build_server(auth_servicer=AuthServicer())
        self._server.start()
        logger.info("Auth gRPC server started")

    def block_until_shutdown(self) -> None:
        assert self._server is not None, "Server not started"
        try:
            self._server.wait_for_termination()
        except KeyboardInterrupt:
            logger.info("Shutting down Auth gRPC server...")
            self._server.stop(grace=10.0)
            logger.info("Auth gRPC server stopped")
