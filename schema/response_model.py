from pydantic import BaseModel, Field

class ResponseModel(BaseModel):
    prediction_category: str = Field(...)
    confidence: float = Field(...)
    class_probabilities: dict[str, float] = Field(...)