import datetime
import jwt

class JWT_handler():

    def __init__(self, private_key_pem: bytes, public_key_pem: bytes):
        self.private_key_pem = private_key_pem
        self.public_key_pem = public_key_pem

    def create_access_token(
        self,
        subject: str,
        expires_days: int = 15,
    ) -> str:
        now = datetime.datetime.now(datetime.timezone.utc)
        payload = {
            "sub": subject,
            "iat": now,
            "exp": now + datetime.timedelta(days=expires_days),
        }

        token = jwt.encode(
            payload,
            self.private_key_pem,
            algorithm="RS256",
        )
        return token

    def verify_access_token(
        self,
        token: str,
        
    ) -> dict:
        payload = jwt.decode(
            token,
            self.public_key_pem,
            algorithms=["RSA256"],
        )
        return payload