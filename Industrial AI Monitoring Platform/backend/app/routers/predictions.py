from fastapi import APIRouter, HTTPException

from app.ml_model import predict_failure
from app.schemas import PredictionRequest, PredictionResponse


router = APIRouter(
    prefix="/api",
    tags=["ML Predictions"],
)


@router.post(
    "/predict",
    response_model=PredictionResponse,
)
def predict(request: PredictionRequest):

    try:
        probability, status = predict_failure(
            temperature=request.temperature,
            vibration=request.vibration,
            pressure=request.pressure,
            rpm=request.rpm,
            current=request.current,
            humidity=request.humidity,
        )

    except RuntimeError as exc:
        raise HTTPException(
            status_code=503,
            detail=str(exc),
        )

    return PredictionResponse(
        failure_probability=probability,
        status=status,
    )