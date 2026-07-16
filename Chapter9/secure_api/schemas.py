"""
Chapter 9 - Excessive data exposure & mass assignment.
Pydantic response/request models act as an allow-list in both directions.
"""
from pydantic import BaseModel, ConfigDict


class UserPublic(BaseModel):
    # Response model: only safe fields leave the API (no ssn/balance).
    id: int
    username: str
    email: str


class UserCreate(BaseModel):
    # Request model: forbids unexpected fields, blocking mass assignment.
    model_config = ConfigDict(extra="forbid")
    username: str
    email: str
    password: str
