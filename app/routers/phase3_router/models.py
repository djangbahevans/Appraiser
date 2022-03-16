from pydantic import BaseModel


class Competency(BaseModel):
    category: str
    sub: str
    main: str
    weight: float
    competency_id: int
