from pydantic import BaseModel


class UserCreateForm(BaseModel):
    name: str
    email: str

# will tell the Pydantic model to read the data even if it is not a dict
# (i.e. attributes)
    class Config:       
        orm_mode = True


    