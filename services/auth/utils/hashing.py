import bcrypt


def verify_hash(raw_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(raw_password.encode(), hashed_password.encode())

def create_hash(raw_password: str)-> str:
    return bcrypt.hashpw(raw_password.encode(), bcrypt.gensalt()).decode()