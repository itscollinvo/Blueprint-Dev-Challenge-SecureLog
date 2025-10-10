from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.middleware.cors import CORSMiddleware  # Import CORS
from pydantic import BaseModel
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import base64
import uuid
import time
import os
import databases

# PostgreSQL URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@postgres:5432/securelog")
database = databases.Database(DATABASE_URL)

app = FastAPI()

# Add CORS middleware
# This will allow your frontend on localhost:3000 to communicate with your backend on localhost:8000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, you can restrict this to ["http://localhost:3000"] in production
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Payload model
class Payload(BaseModel):
    key: str  # RSA key in PEM format
    data: str  # plaintext for encrypt or ciphertext for decrypt


# Create logs table on startup
CREATE_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS logs (
    id VARCHAR PRIMARY KEY,
    timestamp BIGINT,
    ip VARCHAR,
    data TEXT
);
"""

@app.on_event("startup")
async def startup():
    await database.connect()
    await database.execute(CREATE_TABLE_QUERY)

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


# Utility: log requests
async def log_request(ip: str, data: str):
    query = """
    INSERT INTO logs (id, timestamp, ip, data)
    VALUES (:id, :timestamp, :ip, :data)
    """
    values = {
        "id": str(uuid.uuid4()),
        "timestamp": int(time.time()),
        "ip": ip,
        "data": data
    }
    await database.execute(query=query, values=values)


@app.post("/api/v1/encrypt")
async def encrypt(payload: Payload, request: Request):
    # Load public key
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

    # Log request
    await log_request(str(request.client.host), payload.data)

    return {"data": base64.b64encode(ciphertext).decode()}


@app.post("/api/v1/decrypt")
async def decrypt(payload: Payload, request: Request):
    # Load private key
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

    # Log request
    await log_request(str(request.client.host), plaintext.decode())

    return {"data": plaintext.decode()}


@app.get("/api/v1/logs")
async def get_logs(size: int = Query(10, ge=1), offset: int = Query(0, ge=0)):
    query = """
    SELECT * FROM logs
    ORDER BY timestamp DESC
    LIMIT :size OFFSET :offset
    """
    logs = await database.fetch_all(query=query, values={"size": size, "offset": offset})
    return [
        {
            "id": log["id"],
            "timestamp": log["timestamp"],
            "ip": log["ip"],
            "data": log["data"]
        } for log in logs
    ]
