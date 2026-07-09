from typing import Optional
from itertools import filterfalse
from pydantic import BaseModel, Field


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


class UsersDAO():
    def __init__(self):
        self.users_db = {
            "johndoe": {
                "username": "johndoe",
                "full_name": "John Doe",
                "email": "johndoe@example.com",
                "hashed_password": "fakehashedsecret",
                "disabled": False
            },
            "alice": {
                "username": "alice",
                "full_name": "Alice Wonderson",
                "email": "alice@example.com",
                "hashed_password": "fakehashedsecret2",
                "disabled": False
            }
        }

    def get_user(self, username: str):
        if username in self.users_db:
            user_dict = self.users_db[username]
            return UserInDB(**user_dict)

    def hash_password(self, password: str):
        return "fakehashed" + password

    def decode_token(self, token):
        # This doesn't provide any security at all
        # Check the next version
        user = self.get_user(token)
        return user


class Item(BaseModel):
    id: int = Field(1)
    item_name: str


class ItemsDAO():
    def __init__(self):
        self.items_db = [
            Item(id=1, item_name="Foo"),
            Item(id=2, item_name="Bar"),
            Item(id=3, item_name="Baz")
        ]

    def create_item(self, item):
        if isinstance(item, Item):
            item = [i for i in self.items_db if i.id == item.id]
            if len(item) > 0:
                return None
            else:
                self.items_db.append(item)
                return item.dict()

    def delete_item(self, item_id):
        self.items_db[:] = filterfalse(
            lambda x: x.id == item_id, self.items_db)

    def get_all_items(self):
        items = [i.dict() for i in self.items_db]
        return items

    def get_item(self, item_id):
        item = [i for i in self.items_db if i.id == item_id]
        if len(item) > 0:
            return item[0].dict()
        else:
            return {}
