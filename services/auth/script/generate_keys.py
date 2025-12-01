from pathlib import Path
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

base = Path(__file__).resolve().parent.parent
private_key_path = base / "jwt_private_key.pem"
public_key_path = base / "jwt_public_key.pem"

def generate_public_key_from_private(private_key_pem: bytes) -> bytes:
    private_key = serialization.load_pem_private_key(
        private_key_pem,
        password=None,
    )
    public_key = private_key.public_key()

    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return public_pem

def generate_rsa_keypair(
    private_key_path: Path = private_key_path,
    public_key_path: Path = public_key_path,
) -> None:
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(), 
    )
    private_key_path.write_bytes(private_pem)

    public_pem = generate_public_key_from_private(private_pem)
    public_key_path.write_bytes(public_pem)

generate_rsa_keypair()
