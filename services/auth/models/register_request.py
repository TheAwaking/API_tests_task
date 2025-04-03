from pydantic import BaseModel, EmailStr, ConfigDict, model_validator


class RegisterRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    username: str
    password: str
    password_repeat: str
    email: EmailStr

    # @model_validator(mode='after')
    # def check_passwords_match(cls, values):
    #     password = values.get('password')
    #     password_repeat = values.get('password_repeat')
    #
    #     if password != password_repeat:
    #         raise ValueError('Passwords do not match')
    #
    #     return values
