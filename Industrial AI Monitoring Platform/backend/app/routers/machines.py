from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import SensorReading
from app.schemas import (
    SensorReadingCreate,
    SensorReadingResponse,
)
from app.ml_model import predict_failure


router = APIRouter(
    prefix="/api/machines",
    tags=["Machines"],
)


@router.get("", response_model=list[str])
def get_machines(db: Session = Depends(get_db)):
    """
    Return unique machine IDs that have sensor data.
    """

    machines = (
        db.query(SensorReading.machine_id)
        .distinct()
        .order_by(SensorReading.machine_id)
        .all()
    )

    return [machine[0] for machine in machines]


@router.post(
    "/readings",
    response_model=SensorReadingResponse,
)
def create_reading(
    reading: SensorReadingCreate,
    db: Session = Depends(get_db),
):
    probability, _ = predict_failure(
        temperature=reading.temperature,
        vibration=reading.vibration,
        pressure=reading.pressure,
        rpm=reading.rpm,
        current=reading.current,
        humidity=reading.humidity,
    )

    db_reading = SensorReading(
        machine_id=reading.machine_id,
        temperature=reading.temperature,
        vibration=reading.vibration,
        pressure=reading.pressure,
        rpm=reading.rpm,
        current=reading.current,
        humidity=reading.humidity,
        failure_probability=probability,
    )

    db.add(db_reading)
    db.commit()
    db.refresh(db_reading)

    return db_reading


@router.get(
    "/{machine_id}/readings",
    response_model=list[SensorReadingResponse],
)
def get_readings(
    machine_id: str,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    return (
        db.query(SensorReading)
        .filter(
            SensorReading.machine_id == machine_id
        )
        .order_by(
            SensorReading.timestamp.desc()
        )
        .limit(limit)
        .all()
    )