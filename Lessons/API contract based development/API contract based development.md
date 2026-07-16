# API contract based development
In this lesson, you will learn ...

## Setup
For this lesson we will primarily use the [OpenAPI Generator](https://openapi-generator.tech/) to generate code from an OpenAPI specification. You can install this locally using the instructions [here](https://openapi-generator.tech/docs/installation) or simply use Docker to run it in a container with a mounted volume.

```bash
docker run --rm -v ${PWD}:/local openapitools/openapi-generator-cli generate \
    -i /local/PhotoManager.json \
    -g python-flask \
    -o /local/out/python-flask
```

## Instructions
You have two choices in this exercise: either use one of the existing OpenAPI specifications such as Pixi [here](../../OAS%20Files/PhotoManager.json) or create your own using the [Swagger editor](https://editor.swagger.io/) or [Stoplight](https://stoplight.io/).

Once you have an OpenAPI specification, pick a language of your choosing and pick an appropriate server generator from the list [here](https://openapi-generator.tech/docs/generators). 

Use the OpenAPI Generator CLI to generator a server stub for your chosen language, and firstly examine the code to understand what has been implemented, and what remains to be implemented. If you are feeling lucky, try to build the server and run it either in Docker or locally.

## Further Reading
* [OpenAPI Generator](https://openapi-generator.tech/)
* [OpenAPI version 3.1 specification](https://spec.openapis.org/oas/v3.1.0#security-scheme-object)
* [Swagger editor](https://editor.swagger.io/)