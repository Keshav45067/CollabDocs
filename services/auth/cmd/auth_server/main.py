

import asyncio
import signal
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

async def main():
    cnfg = config.Config()
    server = AuthServer(cnfg)
    await server.start()

    loop = asyncio.get_running_loop()
    shutdown_event = asyncio.Event()

    def _on_signal() -> None:
        logging.info("Received shutdown signal, initiating graceful shutdown...")
        shutdown_event.set()

    loop.add_signal_handler(signal.SIGINT, _on_signal)
    loop.add_signal_handler(signal.SIGTERM, _on_signal)

    await shutdown_event.wait()
    await server.stop(grace=10.0)
    

if __name__ == "__main__":
    asyncio.run(main())