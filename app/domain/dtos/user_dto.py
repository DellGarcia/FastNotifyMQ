import re
from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator, ConfigDict


class Validate:

    @classmethod
    def phone(cls, phone):
        phone_pattern = re.compile(r'^(\d{10,11}|\(\d{2}\)\d{8,9}|\(\d{2}\)\d{4,5}-\d{4})$')
        if not phone_pattern.match(phone):
            raise ValueError('Phone number must have 10 or 11 digits')
        return phone


class UserDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    password: str
    phone: str

class UserResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    phone: str



class UserCreateDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    email: EmailStr
    password: str
    phone: str

    @field_validator('phone')
    def validate_phone(cls, phone):
        return Validate.phone(phone)


class UserUpdateDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    phone: Optional[str] = None

    @field_validator('phone')
    def validate_phone(cls, phone):
        return Validate.phone(phone)