from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2AuthorizationCodeBearer
from starlette.requests import Request
from oauthlib.oauth2 import WebApplicationClient
import os, json
import requests
import uvicorn

import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Initialize FastAPI app
app = FastAPI()

# Google OAuth 2.0 information
# TODO Fix this rather unfortunate Git commit by revoking and re-issuing these, and using 1Password
GOOGLE_CLIENT_ID = "55590460044-t2q069rbrgjrs0l3hejkclpquuomco2e.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

# OAuth 2.0 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

# OAuth2AuthorizationCodeBearer instance
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://accounts.google.com/o/oauth2/auth",
    tokenUrl="https://oauth2.googleapis.com/token",
    refreshUrl="https://oauth2.googleapis.com/token",
    scopes={
        "openid": "Access your openid",
        "email": "Access your email",
        "profile": "Access your profile"
    }
)

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

@app.get("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide scopes
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri="http://localhost:3000/auth/callback",
        scope=["openid", "email", "profile"],
    )
    # return {"login_url": request_uri}
    return RedirectResponse(url=request_uri, status_code=status.HTTP_302_FOUND)

@app.get("/auth/callback")
async def callback(request: Request):
    # Extract the authorization code from the query parameters
    code = request.query_params.get('code')

    if not code:
        raise HTTPException(status_code=400, detail="Missing authorization code")

    # Now exchange the code for a token
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url._url,
        redirect_url=request.url_for('callback'),
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now you can use these tokens to access Google APIs or OIDC
    # TODO Decode the token and pretty it up
    return {"token": token_response.json()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
