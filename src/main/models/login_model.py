from pydantic import BaseModel


class AccountRequestBody(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
