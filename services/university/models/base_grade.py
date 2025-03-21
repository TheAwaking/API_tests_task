from pydantic import ConfigDict, BaseModel


class BaseGrade(BaseModel):
    model_config = ConfigDict(extra="forbid")

    count: int
    min: int
    max: int
    avg: int
