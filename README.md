
+-------------------+       +-----------------+       +--------------------+
|    React (Web)    | --->  |  FastAPI (App)  | --->  |  PostgreSQL (DB)   |
|  localhost:3000   |       | localhost:8000  |       | localhost:5432     |
|  User Interface   |       |  API + Logging  |       |   Stores requests  |
+-------------------+       +-----------------+       +--------------------+

Web (frontend) @ Port 3000
located in web/
Built using React + Fetch API
Allows users to:
    Enter encryption/decryption keys
    Send request to FastAPI backend
    view encrypted/decrypted responses
    view request logs


Server (backend) @ Port 8000
Located in server/
Built using FastAPi
Handles encryption, decryption, and logging into PostgreSQL
RESTful endpoints:
    /api/v1/encrypt
    /api/v1/decrypt
    /api/v1/logs


Database (PostgreSQL)
    stores request logs
    automatically created using docker

Credentials:
    POSTGRES_USER=user
    POSTGRES_PASSWORD=password
    POSTGRES_DB=securelog
    
--------

1. Prerequsites:
Docker & Docker Compose installed
Node.js
Python 3.11+
2. Clone Repo
git clone https://github.com/itscollinvo/Blueprint-Dev-Challenge-SecureLog.git
cd Blueprint-Dev-Challenge-SecureLog
3. Run application with Docker
docker compose up --build
Frontend: http://localhost:3000
Backend: http://localhost:8000/docs  (interactive api docs)
PostgreSQL: localhost:5432

Sample API Request:

POST /api/v1/encrypt

Request Body:

{
    "key": "-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA03t7OmyfZSwf62+khWFo
yioELOwBlhptXvrCqxHIvMTfNkYE2ql7Kohwr+MbjHZ6Qs7bUJ2GOWqBeAtap7vF
kd+UKI3HdIxH/Lh6eer5vM33oPQzwTuGoQzPx2fjX5vUxpXgy6kPE8ghndObeIQi
c4LVSTJcluoL+KQWfubXji35J+EWeoIs5GTRiqlSB4r0hX5E79N/rnbO2LHl5EfX
Y1sRJwiEG4Sc9kK2KpcB0PjV/Bo2nRajuaX4xcJhz0Ae8Fo5STokDjN4oCdP106H
Q5r081iq2VaV5MiGDrWJGJtAylWpFCYIH26jmZiAxF5vpPt3y02NQ92CHgHFZAxy
mwIDAQAB
-----END PUBLIC KEY-----"
    "data": "<Type any text in here>"
}

Response:

{
    data: "<encrpyted data>"
}


POST /api/v1/decrypt

{
    "key": "-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEA03t7OmyfZSwf62+khWFoyioELOwBlhptXvrCqxHIvMTfNkYE
2ql7Kohwr+MbjHZ6Qs7bUJ2GOWqBeAtap7vFkd+UKI3HdIxH/Lh6eer5vM33oPQz
wTuGoQzPx2fjX5vUxpXgy6kPE8ghndObeIQic4LVSTJcluoL+KQWfubXji35J+EW
eoIs5GTRiqlSB4r0hX5E79N/rnbO2LHl5EfXY1sRJwiEG4Sc9kK2KpcB0PjV/Bo2
nRajuaX4xcJhz0Ae8Fo5STokDjN4oCdP106HQ5r081iq2VaV5MiGDrWJGJtAylWp
FCYIH26jmZiAxF5vpPt3y02NQ92CHgHFZAxymwIDAQABAoIBAExbxnem5rqR/wh0
LBQYwsxT9WP+5ue6rQjhQ86ewjseXnXrPC9ziEwoLX/kYXsLAEQFCn0GE4PBp/Of
LeFoVALClm06G+1CBXADb/17USbRu3p7EgDQLGEUDiWypg9MZbw6O4tthEshNLoW
wIj4NLQ+ZiJis7mt0hq5rIGved8UpE4Nfb5KF/bjnS1YAc0+WqnE0GQPMOQywULa
18E3wWnBau+tK1h0DYvVSeaoI/yABjBmnox/jhqFbs6RnedHG2uP6JmavCwYNTMY
ijs8/UcqqYBXAhyrIVqi6S8mO2XMCLhgTXbe5oj17CoOkky5DD/4RVBESC8aVNzv
LQeIXbkCgYEA7xtHlftFcMutTtUc+7r0LToKttOI+OzgT/dRv6b2XeVpKcWJj917
PuY39y3n/vMOMaNBW3wqqJWRncxLPiU3WXRIXYEvsTpUPtkftX3W70poD8oornEZ
aY5mq4pKr5O08Mp5neGpMlM+s9zktsEEs4m3HxqYCKVPtdGPmK0TE4cCgYEA4myQ
Bu5YhmHrfj3WsQ2y6yr1Qd+U7+XSt7mz5nPZZHG+UDkANtWyqtflNV1QkaH4gQJM
8JoqGwiEz5lF2EKFocPpkYGee0dd84o7a52ZpRsB7E0WuwMrT70D5Wv2gDNdvnao
eSqK+HvEj4yjYmD1vS1ncx0+0pLoVAlTvg3+lU0CgYBmuoS2Fn/OJ2Ptc7iBGuCf
sck6pYW61SLGmI6h1d0RmGfnT3x7t/+klYrEAxAixFB72RVSdfVp+uDWOBi3uYuf
Pkt9COzxqwrY+bYa5tb6djBhYEy8LdFqPYk0+DSAXOinb4Zy46oq+gL9idEmB6W6
cVeg4G8jf8rQZhnY0btZbwKBgAptSWyoSTdXBws3Oc3JfbXKsqSn8SnjAYMocBpq
t1YizsrO9S2RRbsMWifM9krelJ0MSBLEZq/8AnG08zx0Q8chSH5E49F1heQTN41L
IqoxxjLlkehmyvXPFIDaKe3Zb7W3rSZ3SRMMUA70QQnkwSxHDP6GGECGN2C3VT3p
UxH5AoGBAI3p4kudi9DXwIp/schLDIMksItHdDyprA4zIVm2w2bXF8F+LmY6RJkV
Ba2TW8k+xFI7t664cord7vkou7NUGMC3C/vy+C6zQD+H+GeUtAPSq0lO/cQfnKrG
b1OIbGtuMMqdtnGWEa542PNmishNA8C67y4yNbxzZ72iYX/B057U
-----END RSA PRIVATE KEY-----"
    "data": "<Encrypted data from POST /api/v1/encrypt response>
}

Response:

{
    "data": "<your decrypted message>"
}



How it works:
1. User input:
    A user enters a key and payload in the frontend
2. API call:
    The fronend calls FastAPI with /encrypt or /decrypt
3. Processing:
    The backend encrypts/decrypts using the provided key, logs the request in PostgreSQL, and returns the result.
4. Display:
    The frontend displays the response and offers a log view
