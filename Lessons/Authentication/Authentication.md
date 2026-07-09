# Authentication
In this lesson, you will learn more about authentication, including the common types of authentication, how to implement authentication, and how to test authentication. You will specifically focus on OAuth2 and JWTs as core to modern authentication solutions.

## Setup
You will need a modern Python environment (> 3.6) and the following packages installed from the [requirements](../requirements.txt) file.

## Instructions
### Step 1: Play with the OAuth2 flows on the OAuth2 playground
User the [OAuth2 playground](https://www.oauth.com/playground/index.html) tool to work through OAuth2 scenarios to understand how they work.

### Step 2: Play with the OIDC flows on the OIDC playground
Use the [OIDC playground](https://openidconnect.net/) tool to work through OIDC scenarios to understand how they work.

### Step 3: Create and validate JWTs using JWT.io to understand how they work
Use the [JWT io](https://jwt.io/) tool to create and validate JWTs to understand how they work. 

### Step 4: Use the script provided to create JWTs
Use the [jwt_tool.py](./jwt_tools.py) script to generate and verify JWTs. Try adjusting the expiry time and check it detects expiration, and see if you can tamper with the data. Use the JWT.io tool to independently verify the JWTs.

## Further Reading
* [OAuth2 playground](https://www.oauth.com/playground/index.html)
* [OIDC playground](https://openidconnect.net/)
* [JWT io](https://jwt.io/)
* [Introduction to OAuth 2.0 and OpenID Connect](https://pragmaticwebsecurity.com/talks/introductionoauth)
* [Philippe De Ryck's cheat sheets](https://pragmaticwebsecurity.com/cheatsheets.html)
