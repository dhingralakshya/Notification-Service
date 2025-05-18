# for data validation uisng pydantic
from pydantic import BaseModel

# schema to create request using post method
class NotificationCreate(BaseModel):
    user_id: str
    notif_type: str  # "email", "sms", "in_app"
    content: str

# schema to get notifications for user using user_id
class NotificationOut(BaseModel):
    id: int
    user_id: str
    notif_type: str
    content: str
    status: str

    class Config:
        orm_mode = True # convert SQLAlchemy objects to Pydantic models.
