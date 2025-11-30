

from config import config
from internal.server.auth_server import AuthServer
import logging
import sys

logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
    force=True, 
)

def main():
    cnfg = config.Config()
    server = AuthServer(cnfg)
    server.start()
    server.block_until_shutdown()

if __name__ == "__main__":
    main()