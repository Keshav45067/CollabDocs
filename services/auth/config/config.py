class Config:
    def __init__(self, host='0.0.0.0', port='50051', is_production=False):
        self.host: str = host
        self.port: str = port
        self.is_production: bool = is_production

    def address(self)->str:
        return f"{self.host}:{self.port}"