from fastapi import Depends, FastAPI, HTTPException, status, Request, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.responses import PlainTextResponse, RedirectResponse
from pydantic import BaseModel
import casbin
import uvicorn
import os 

from utils import ItemsDAO, UsersDAO, UserInDB, User
from utils import Item

app = FastAPI()
items_dao = ItemsDAO()
users_dao = UsersDAO()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = users_dao.decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

async def get_current_active_user(curr_user: User = Depends(get_current_user)):
    if curr_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user")
    return curr_user

async def get_current_user_authorization(req: Request, curr_user: User = Depends(get_current_active_user)):
    # TODO: Fix this mess with a relative path - must be run from root of repository 
    e = casbin.Enforcer("./Lessons/Authorization/model.conf", "./Lessons/Authorization/policy.csv")
    sub = curr_user.username
    obj = req.url.path
    act = req.method
    if not(e.enforce(sub, obj, act)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Method not authorized for this user")
    return curr_user

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_dao.get_user(form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password")
    hashed_password = users_dao.hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password")
    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    response = RedirectResponse(url='/docs')
    return response


@app.get("/items")
async def read_all_items(req: Request, curr_user: User = Depends(get_current_active_user)):
    return items_dao.get_all_items()


@app.get("/items/{item_id}")
async def read_item(item_id: int, req: Request, curr_user: User = Depends(get_current_active_user)):
    return items_dao.get_item(item_id)


@app.post("/items/")
async def create_item(item: Item, req: Request, curr_user: User = Depends(get_current_active_user)):
    answer = items_dao.create_item(item)
    if not (answer):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Item with given id already exists")
    else:
        return answer


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int, req: Request, curr_user: User = Depends(get_current_active_user)):
    items_dao.delete_item(item_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
