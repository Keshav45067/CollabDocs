import os
from pathlib import Path
from dotenv import load_dotenv
class Config:
    def __init__(self):
        load_dotenv()
        self.host: str = self.loadEnv("HOST")
        self.port: str = self.loadEnv("PORT")
        self.is_production: bool = self.getBool("IS_PRODUCTION")
        self.async_db_api: str = self.loadEnv("ASYNC_DB_API")
        self.user: str = self.loadEnv("POSTGRES_USER")
        self.password: str = self.loadEnv("POSTGRES_PASSWORD")
        self.host: str = self.loadEnv("POSTGRES_HOST")
        self.db_port: str = self.loadEnv("POSTGRES_PORT")
        self.db: str = self.loadEnv("POSTGRES_DB")
        self.jwt_public_key: bytes = self.load_public_key_pem()
        self.jwt_private_key: bytes = self.load_private_key_pem()

    def address(self)->str:
        return f"{self.host}:{self.port}"

    def loadEnv(self, key: str):
        val: str = os.getenv(key)
        assert val != "", f"environment variable '{key}' not provided"
        return val
            
    
    def build_connection_string(self) -> str:
        db_api: str = self.async_db_api
        user: str = self.user
        password: str = self.password
        host: str = self.host
        db_port: str = self.db_port
        db: str = self.db
        return f"postgresql+{db_api}://{user}:{password}@{host}:{db_port}/{db}"

    def load_private_key_pem(self) -> bytes:
        base = Path(__file__).resolve().parent.parent
        path = base / "jwt_private_key.pem"
        return path.read_bytes()


    def load_public_key_pem(self) -> bytes:
        base = Path(__file__).resolve().parent.parent
        path = base / "jwt_public_key.pem"
        return path.read_bytes()

    def getBool(self, key: str)->bool:
        val = self.loadEnv(key)
        assert ((val == "True") | (val == "False")), "Invalid Value of IS_PRODUCTION variable"
        if val == "False":
            return False
        if val == "True":
            return True;
        
