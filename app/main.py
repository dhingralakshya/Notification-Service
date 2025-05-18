# define endpoints and database dependency
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Notification, SessionLocal, init_db
from schemas import NotificationCreate, NotificationOut
import asyncio
import aio_pika
import json


init_db() # to ensure database exist on startup to avoid error in case table is not created before hand

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

RABBITMQ_URL = "amqp://guest:guest@localhost/"

@app.post("/notifications/", response_model=NotificationOut)
async def create_notification(notif: NotificationCreate, db: Session = Depends(get_db)):
    # Save notification as "pending"(default)
    db_notif = Notification(
        user_id=notif.user_id,
        notif_type=notif.notif_type,
        content=notif.content,
        status="pending"
    )
    db.add(db_notif)
    db.commit()
    db.refresh(db_notif)

    # Send to queue
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        await channel.default_exchange.publish(
            aio_pika.Message(body=json.dumps({
                "id": db_notif.id,
                "user_id": notif.user_id,
                "notif_type": notif.notif_type,
                "content": notif.content
            }).encode()),
            routing_key="notifications"
        )
    return db_notif

@app.get("/users/{user_id}/notifications", response_model=list[NotificationOut])
def get_notifications(user_id: str, db: Session = Depends(get_db)):
    notifs = db.query(Notification).filter(Notification.user_id == user_id).all()
    return notifs
