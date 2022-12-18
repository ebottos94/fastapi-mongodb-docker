from pydantic import BaseModel, Field


class IngestionSchema(BaseModel):
    key: int = Field(..., ge=1, le=6)
    payload: str = Field(..., max_length=255, min_length=10)

    class Config:
        schema_extra = {
            "example": {
                "key": 1,
                "payload": "Stringa Esempio",
            }
        }
