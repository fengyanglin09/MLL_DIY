# Security with python backend + Angular

### Objective:
1. Stateless Authentication using JWT
2. Secure communication between Angular frontend + Python backend

### Stacks and Architecture
| Layer       | Technology                        | Role                                    |
|-------------|-----------------------------------|-----------------------------------------|
| Frontend    | Angular                           | User interface, calls secured APIs      |
| Backend     | Python (FastAPI or Django)        | Resource server, validates access tokens |
| Auth        | Azure Entra ID                    | Identity provider & OAuth 2.0 / OpenID Connect |
| Token Type  | JWT (access token issued by Azure Entra ID) | Used for auth between Angular ↔ Backend |


### Authentication Flow (OAuth2/OIDC + JWT)
1. User logs in via Angular (using Entra ID login page)
2. Angular receives an access_token (and optionally id_token) from Entra ID
3. Angular sends JWT (in Authorization: Bearer <token>) to Python backend
4. Python backend validates the token (signature, expiration, audience, issuer)
5. Backend processes request if token is valid

### Token Validation (Backend ↔ Azure Entra ID)
1. **User Login**
   - User logs in via the Angular frontend using **MSAL** or an **OAuth flow** to sign in.
   
2. **Token Issuance**
   - **Azure Entra ID** issues an **access token** (JWT).

3. **Token Usage**
   - The access token is sent with every API request from the frontend to the backend in the HTTP header:
     ```makefile
     Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOi...
     ```
4. **Backend extracts the JWT**
   -  In your FastAPI route (or Django middleware), grab the Authorization header and extract the token.

5. **Backend fetches Azure's public keys (JWKS)**
   -  Azure Entra ID publishes a JSON Web Key Set (JWKS) used to verify JWT signatures.

6. **Backend verifies the token**
   # JWT Validation Checklist

| Check | Description |
|-------|-------------|
| ✅ Signature | Use `kid` in JWT header to select the correct public key from JWKS and verify |
| ✅ exp claim | Ensure token is not expired |
| ✅ aud claim | Must match your backend app’s client ID (Azure App Registration) |
| ✅ iss claim | Must match issuer URL (`https://login.microsoftonline.com/<tenant_id>/v2.0`) |
| ✅ nbf / iat | (Optional) Ensure the token is not used before it's valid |