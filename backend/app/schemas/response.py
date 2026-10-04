from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel

T = TypeVar("T")

class ErrorDetail(BaseModel):
    code: str
    message: str

class APIResponse(BaseModel, Generic[T]):
    success: bool = True
    message: Optional[str] = None
    data: Optional[T] = None
    error: Optional[ErrorDetail] = None

    @classmethod
    def ok(cls, data: Optional[T] = None, message: Optional[str] = None):
        return cls(success=True, data=data, message=message)

    @classmethod
    def fail(cls, code: str, message: str):
        return cls(success=False, error=ErrorDetail(code=code, message=message))
