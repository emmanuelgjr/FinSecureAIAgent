from cryptography.fernet import Fernet
from jose import JWTError, jwt
from datetime import datetime, timedelta

# 🔐 Shared secret key used across the entire app
SECRET_KEY = "super-secure-shared-key"  # You can change this to something long & random
ALGORITHM = "HS256"

class A2ASecurity:
    def __init__(self, secret_key: str = SECRET_KEY):
        self.fernet = Fernet(Fernet.generate_key())
        self.secret_key = secret_key
        self.algorithm = ALGORITHM

    def encrypt_data(self, data: str) -> bytes:
        return self.fernet.encrypt(data.encode())

    def decrypt_data(self, encrypted_data: bytes) -> str:
        return self.fernet.decrypt(encrypted_data).decode()

    def create_jwt_token(self, agent_id: str, expires_in_minutes=60) -> str:
        payload = {
            "agent_id": agent_id,
            "exp": datetime.utcnow() + timedelta(minutes=expires_in_minutes)
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def verify_jwt_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except JWTError:
            return None

if __name__ == "__main__":
    security = A2ASecurity()
    encrypted = security.encrypt_data("Sensitive financial data")
    print("Encrypted:", encrypted)

    decrypted = security.decrypt_data(encrypted)
    print("Decrypted:", decrypted)

    token = security.create_jwt_token("agent1")
    print("JWT Token:", token)

    payload = security.verify_jwt_token(token)
    print("Verified JWT Payload:", payload)
