from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import base64

app = FastAPI()

# Payload model
class Payload(BaseModel):
    key: str  # RSA key in PEM format
    data: str  # plaintext for encrypt, ciphertext for decrypt


@app.post("/api/v1/encrypt")
async def encrypt(payload: Payload):
    # Load the public key
    try:
        public_key = serialization.load_pem_public_key(payload.key.encode())
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid public key format")

    # Encrypt
    try:
        ciphertext = public_key.encrypt(
            payload.data.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Encryption failed")

    return {"data": base64.b64encode(ciphertext).decode()}



@app.post("/api/v1/decrypt")
async def decrypt(payload: Payload):
    # Load the private key
    try:
        private_key = serialization.load_pem_private_key(payload.key.encode(), password=None)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid private key format")

    # Decrypt
    try:
        ct_bytes = base64.b64decode(payload.data)
        plaintext = private_key.decrypt(
            ct_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    except Exception:
        raise HTTPException(status_code=400, detail="Decryption failed or key mismatch")

    return {"data": plaintext.decode()}
