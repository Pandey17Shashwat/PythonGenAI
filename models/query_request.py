from typing import Optional

from pydantic import BaseModel


class QueryRequest(BaseModel):
    query: str
    format: Optional[str] = "text"