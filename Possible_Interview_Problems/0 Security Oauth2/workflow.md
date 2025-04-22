1. The Angular frontend requests authorization from Azure AD.
2. Azure AD redirects the user to the login page.
3. The user authenticates with Azure AD.
4. Azure AD redirects the user back to the Angular frontend with an authorization code.
5. The Angular frontend sends the authorization code to the FastAPI backend.
6. The FastAPI backend requests an access token from Azure AD.
7. Azure AD issues an access token to the FastAPI backend.
8. The FastAPI backend validates the access token.
9. The FastAPI backend returns protected resources to the Angular frontend.