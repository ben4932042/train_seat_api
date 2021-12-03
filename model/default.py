from typing import Optional
from pydantic import BaseModel

class DefaultSuccessReturn(BaseModel):
    message: Optional[str] = 'success'

