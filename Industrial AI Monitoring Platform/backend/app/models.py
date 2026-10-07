from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String

from app.database import Base


class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True, index=True)

    machine_id = Column(String(50), nullable=False, index=True)

    timestamp = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    temperature = Column(Float, nullable=False)
    vibration = Column(Float, nullable=False)
    pressure = Column(Float, nullable=False)
    rpm = Column(Float, nullable=False)
    current = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)

    failure_probability = Column(Float, nullable=True)