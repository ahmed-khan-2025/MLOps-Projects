from datetime import datetime

from pydantic import BaseModel


class SensorReadingCreate(BaseModel):
    machine_id: str

    temperature: float
    vibration: float
    pressure: float
    rpm: float
    current: float
    humidity: float


class SensorReadingResponse(BaseModel):
    id: int
    machine_id: str
    timestamp: datetime

    temperature: float
    vibration: float
    pressure: float
    rpm: float
    current: float
    humidity: float

    failure_probability: float | None = None

    class Config:
        from_attributes = True


class PredictionRequest(BaseModel):
    temperature: float
    vibration: float
    pressure: float
    rpm: float
    current: float
    humidity: float


class PredictionResponse(BaseModel):
    failure_probability: float
    status: str