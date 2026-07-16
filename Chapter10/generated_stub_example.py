"""
Chapter 10 - Example of what a generated server stub looks like.
This is a hand-written approximation of the python-fastapi output from petstore.yaml,
showing how the OpenAPI contract maps directly onto typed handlers.
"""
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Petstore", version="1.0.0")


class Pet(BaseModel):
    id: int
    name: str
    tag: str | None = None


PETS = [Pet(id=1, name="Rex", tag="dog"), Pet(id=2, name="Whiskers", tag="cat")]


@app.get("/pets", response_model=list[Pet])
def list_pets() -> list[Pet]:
    return PETS
