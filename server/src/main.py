from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
import base64
import time
import uuid


app = FastAPI()

# pydantic model for request payload
class Payload(BaseModel):
    key: str    # base64-encoded 32 byte key
    data: str   # plaintext for encrypt, ciphertext for decrypt


# base64 decode. exception: invalid input
def decode_raw(s: str) -> bytes:
    try:
        return base64.b64decode(s)
    except Exception: 
        raise HTTPException(status_code=400, detail="Invalid base64 input")

# no need for exception if decode is valid
def encode_raw(b: bytes) -> str:
    return base64.b64encode(b).decode()


@app.post("/api/v1/encrypt")
async def encrypt(payload: Payload, request: Request):
    # convert to byte
    key = decode_raw(payload.key)
    if len(key) != 32:
        raise HTTPException(status_code=400, detail="Key must be 32 bytes")
    
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ct = aesgcm.encrypt(nonce, payload.data.encode(), None)
    encrypted_data = nonce + ct
    # log request to database

    return {"data": encode_raw(encrypted_data)}



@app.post("/api/v1/decrypt")
async def decrypt(payload: Payload, request: Request):
    key = decode_raw(payload.key)
    if len(key) != 32:
        raise HTTPException(status_code=400, detail="Key must be 32 bytes")
    raw = decode_raw(payload.data)
    if len(raw) < 12 + 16: # nonce (12 bytes) + tag (16 bytes)
        raise HTTPException(status_code=400, detail="Ciphertext too short")
    nonce = raw[:12]
    ct = raw[12:]
    aesgcm = AESGCM(key)
    try:
        pt = aesgcm.decrypt(nonce, ct, None)
    except Exception:
        raise HTTPException(status_code=400, detail="Decryption failed or tag mismatch")

    # log request to database here

    return {"data": pt.decode()}




