# API Testing
In this lesson, you will learn how to use specialist API security testing tools to test your APIs runtime behavior, and identify potential security vulnerabilities and deviations from the API contract.

## Setup
For this lesson, you will need the following:
* [Postman](https://www.getpostman.com/) - a popular API testing tool
* [VS Code](https://code.visualstudio.com/) with the [42Crunch OpenAPI plugin](https://marketplace.visualstudio.com/items?itemName=42Crunch.vscode-openapi) installed. You will also need to request a free token from 42Crunch to use the plugin.

## Instructions

### Step 1: Install an API of your choosing 
Use one of the APIs we have worked with in previous lessons, or use the Pixi API application running in Docker from [here](../../Sample%20APIs/Pixi/docker-compose.yaml).

### Step 2: Use Postman to test this API in a few different ways:
* Use individual commands to test the API behavior (use the Postman collection from [here](https://www.postman.com/get-42crunch/workspace/42crunch-api/collection/13761657-2fe8d964-9687-4a95-9e16-2c06e7d5fe7e)
* Use the individual method tests in Postman to verify correct behavior of each method.
* Use the new AI based automated testing to generate API tests using [this](https://danaepp.com/api-security-testing-using-ai-in-postman) article as a guide.
* If time or interest permits, use the _numan_ CLI tool to run the tests from the command line.

### Step 3: Use the 42Crunch OpenAPI plugin to test the API
* Install the plugin and get an activation code by providing your email address.
* Open the Pixi / Photoshop OpenAPI specification in VS Code from [here](../../OAS%20Files/PhotoManager.json).
* Use the plugin to either "Try It" or "Scan It" to run tests, and review the results paying attention to understanding the findings.

## Further Reading
* [API Testing with Postman](https://learning.postman.com/docs/designing-and-developing-your-api/testing-an-api/)
* [Pixi / PhotoManager API on Postman](https://www.postman.com/get-42crunch/workspace/42crunch-api/collection/13761657-2fe8d964-9687-4a95-9e16-2c06e7d5fe7e)
* [42Crunch conformance testing](https://42crunch.com/api-conformance-scan/)
* [42Crunch OpenAPI plugin](https://marketplace.visualstudio.com/items?itemName=42Crunch.vscode-openapi)
* [API Security Testing using AI in Postman](https://danaepp.com/api-security-testing-using-ai-in-postman)
* [Postman numan CLI](https://learning.postman.com/docs/postman-cli/postman-cli-overview/)