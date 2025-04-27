from fastapi import APIRouter
from schemas import (
    BodyTypeEnum, CarConditionEnum,
    DriveTypeEnum, TransmissionEnum, FuelTypeEnum, SteeringSideEnum
)

router = APIRouter(prefix="/enums", tags=["Enums"])

@router.get("/body-types", response_model=list[str])
def get_body_types():
    return list(BodyTypeEnum.__args__)

@router.get("/car-conditions", response_model=list[str])
def get_car_conditions():
    return list(CarConditionEnum.__args__)

@router.get("/drive-types", response_model=list[str])
def get_drive_types():
    return [d.value for d in DriveTypeEnum]

@router.get("/transmissions", response_model=list[str])
def get_transmissions():
    return [t.value for t in TransmissionEnum]

@router.get("/fuel-types", response_model=list[str])
def get_fuel_types():
    return [f.value for f in FuelTypeEnum]

@router.get("/steering-sides", response_model=list[str])
def get_steering_sides():
    return [s.value for s in SteeringSideEnum]