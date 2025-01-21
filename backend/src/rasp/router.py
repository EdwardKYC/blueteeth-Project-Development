from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from src.dependencies import get_db
from src.rasp.models import Rasp, Device
from src.rasp.constants import CardinalDirection
from src.history.service import HistoryService
from src.websockets import WebSocketMessageHandler
from .schemas import RegisterRaspSchema, RegisterDeviceSchema, UpdateDeviceBatterySchema

router = APIRouter(
    prefix="/rasp",
    tags=["Rasp"],
    responses={404: {"description": "Not found"}},
)

websocket_handler = WebSocketMessageHandler()
history = HistoryService()

@router.post("/register-rasp")
async def register_rasp(
    params: RegisterRaspSchema,
    db: Session = Depends(get_db),
):
    facing = params.facing
    cord_x = params.cord_x
    cord_y = params.cord_y

    try:
        validated_facing = CardinalDirection[facing.upper()] 
    except KeyError:
        await history.log_warning(
            db=db,
            action="Register Rasp",
            details=f"Invalid facing value '{facing}' provided for Rasp '{rasp_id}'."
        )
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid facing value '{facing}'. Must be one of {', '.join([d.name for d in CardinalDirection])}"
        )
    
    rasp_count = db.query(Rasp).count()
    rasp_id = f"rasp{rasp_count + 1}"

    new_rasp = Rasp(
        id=rasp_id,
        cord_x=cord_x,
        cord_y=cord_y,
        facing=validated_facing.value,
    )
    db.add(new_rasp)
    db.commit()
    db.refresh(new_rasp)

    await history.log_info(
        db=db,
        action="Register Rasp",
        details=f"Rasp '{rasp_id}' registered at coordinates ({cord_x}, {cord_y}) facing {validated_facing.name}",
    )
    await websocket_handler.register_rasp(rasp=new_rasp)

    return f"Successfully registered Rasp '{rasp_id}"

@router.post("/register-device")
async def register_device(
    params: RegisterDeviceSchema,
    db: Session = Depends(get_db),
):
    rasp_id = params.rasp_id
    battery = params.battery
    cord_x = params.cord_x
    cord_y = params.cord_y

    rasp = db.query(Rasp).filter(Rasp.id == rasp_id).first()
    if not rasp:
        await history.log_warning(
            db=db,
            action="Register Device",
            details=f"Attempt to register a device under a non-existent Rasp ID '{rasp_id}'"
        )
        raise HTTPException(status_code=404, detail=f"Rasp with ID '{rasp_id}' not found")

    device_count = db.query(Device).count()
    new_device_id = f"device{device_count + 1}"

    new_device = Device(
        id=new_device_id,
        battery=battery,
        cord_x=cord_x,
        cord_y=cord_y,
        rasp_id=rasp_id,
    )
    db.add(new_device)
    db.commit()
    db.refresh(new_device)

    await history.log_info(
        db=db,
        action="Register Device",
        details=f"Device {new_device.id} registered at coordinates ({cord_x}, {cord_y}) with battery {battery}% under Rasp '{rasp_id}'",
    )
    await websocket_handler.register_device(device=new_device)

    return f"Successfully registered Device '{new_device.id}"
  

@router.post("/update-device-battery")
async def update_device_battery(
    params: UpdateDeviceBatterySchema,
    db: Session = Depends(get_db),
):
    device_id = params.device_id
    battery = params.battery

    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        await history.log_warning(db=db, action="Update Device Battery", details=f"Device with ID '{device_id}' not found")
        raise HTTPException(status_code=404, detail=f"Device with ID '{device_id}' not found")

    if battery < 0 or battery > 100:
        await history.log_warning(
            db=db,
            action="Update Device Battery",
            details=f"Device '{device_id}' received an out-of-bound battery value: {battery}",
        )
        raise HTTPException(status_code=400, detail="Battery value must be between 0 and 100")

    device.battery = battery
    db.commit()
    db.refresh(device)

    await history.log_info(
        db=db,
        action="Update Device Battery",
        details=f"Device '{device_id}' battery updated to {battery}%",
    )
    await websocket_handler.update_device_battery(device_id=device_id, battery=battery)

    return f"Successfully update the battery of {device_id}"

@router.get("/get-all-devices", response_model=list)
def get_all_devices(db: Session = Depends(get_db)):
    """
    Fetch all devices with basic information and their associated rasp_id.
    """
    devices = db.query(Device).all()
    return [
        {
            "id": device.id,
            "battery": device.battery,
            "cords": {"x": device.cord_x, "y": device.cord_y},
            "rasp_id": device.rasp.id if device.rasp else None
        }
        for device in devices
    ]

@router.get("/get-all-rasps", response_model=list)
def get_all_rasps(db: Session = Depends(get_db)):
    """
    Fetch all rasps with their basic information.
    """
    rasps = db.query(Rasp).all()
    return [
        {
            "id": rasp.id,
            "cords": {"x": rasp.cord_x, "y": rasp.cord_y},
            "facing": rasp.facing
        }
        for rasp in rasps
    ]

@router.delete("/delete-device/{device_id}")
async def delete_device(device_id: str, db: Session = Depends(get_db)):
    """
    Delete a device by its ID.
    """
    device = db.query(Device).filter(Device.id == device_id).first()

    if not device:
        raise HTTPException(status_code=404, detail=f"Device with ID '{device_id}' not found")

    db.delete(device)
    db.commit()

    return {"detail": f"Device '{device_id}' successfully deleted"}