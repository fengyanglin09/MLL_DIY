## Question1 for step 4 - Azure AD redirects the user back to the Angular frontend with an authorization code. what the users would see at this point?

When Azure AD redirects the user back to the Angular frontend with an authorization code, the user will see a brief redirect process, and then they will be taken back to the Angular application.

1. After authenticating with Azure AD, the user will see a brief redirect page (usually a blank page or a page with a loading indicator).
2. The redirect page will contain the authorization code as a query parameter in the URL.
3. The Angular frontend will receive the authorization code and send it to the FastAPI backend to exchange it for an access token.
4. Once the access token is obtained, the Angular frontend will redirect the user to the protected page or resource they were trying to access.


### Example URL
```markdown
http://localhost:4200/callback?code=0.AX4AuthorizationCodeHere...
```

### User experience:
The redirect process should be seamless and quick, so the user might not even notice it. However, if the redirect takes a bit longer, the user might see a brief loading indicator or a blank page.


### Next Steps from getting Authorization code
1. Angular sends the authorization code to the FastAPI backend.
2. The FastAPI sends a request to the Azure AD token endpoint with the authorization code, client ID, client secret, and redirect URI.
3. Azure AD issues an access token to the FastAPI backend
4. The FastAPI backend returns the access token to the Angular frontend.
5. The Angular frontend uses the access token to access protected resources on the FastAPI backend.


### Access token:
Only after the Angular frontend receives the access token can it access protected resources on the FastAPI backend. The access token is what's used to authenticate and authorize the user to access specific resources.

### Angular frontend's role:
The Angular frontend's role is to:
1. Redirect the user to Azure AD for authentication.
2. Receive the authorization code from Azure AD.
3. Send the authorization code to the FastAPI backend.
4. Receive the access token from the FastAPI backend.
5. Use the access token to access protected resources.

### FastAPI backend's role:
The FastAPI backend's role is to:
1. Exchange the authorization code for an access token with Azure AD.
2. Validate the access token on each request.
3. Return protected resources to the Angular frontend if the access token is valid.