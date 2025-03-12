from pydantic import BaseModel, Field

class RegisterRaspSchema(BaseModel):
    cord_x: int = Field(..., description="The X coordinate of the Rasp")
    cord_y: int = Field(..., description="The Y coordinate of the Rasp")
    facing: str = Field(..., description="The cardinal direction the Rasp is facing")
    rasp_id: str = Field(..., min_length=1, max_length=100, description="The associated Rasp ID")

class RegisterDeviceSchema(BaseModel):
    battery: int = Field(..., ge=0, le=100, description="Battery percentage of the device")
    cord_x: int = Field(..., description="The X coordinate of the device")
    cord_y: int = Field(..., description="The Y coordinate of the device")
    rasp_id: str = Field(..., min_length=1, max_length=100, description="The associated Rasp ID")
    device_id: str = Field(..., min_length=1, max_length=100, description="The associated Device ID")

class UpdateDeviceBatterySchema(BaseModel):
    battery: int = Field(..., ge=0, le=100, description="The new battery percentage of the device")
    device_id: str = Field(..., min_length=1, max_length=100, description="The unique ID of the Device")