from pydantic import BaseModel, Field
from typing import Optional, List, Generic, TypeVar, ClassVar
from pydantic.generics import GenericModel

T = TypeVar('T')


class UserSchema(BaseModel):

    first_name: Optional[str]
    second_name: Optional[str]
    password: Optional[str]
    login: Optional[str]


