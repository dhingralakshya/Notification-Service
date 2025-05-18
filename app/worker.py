# background worker that processes the queue and then send notification uisng services
# call the appropriate send function and then update the status to sent or in case of error set to failed
import asyncio
import aio_pika
import json
from models import SessionLocal, Notification
from services import send_email, send_sms, send_in_app

RABBITMQ_URL = "amqp://guest:guest@localhost/"

MAX_RETRIES = 3

async def process_notification(body, channel):
    data = json.loads(body)
    notif_id = data["id"]
    notif_type = data["notif_type"]
    user_id = data["user_id"]
    content = data["content"]
    retries = data.get("retries", 0)  # Default to 0

    db = SessionLocal()
    notif = db.query(Notification).filter(Notification.id == notif_id).first()
    try:
        if notif_type == "email":
            await send_email(user_id, content)
        elif notif_type == "sms":
            await send_sms(user_id, content)
        elif notif_type == "in_app":
            await send_in_app(user_id, content)
        notif.status = "sent"
    except Exception as e:
        if retries < MAX_RETRIES:
            print(f"Retrying notification {notif_id}, attempt {retries + 1}")
            # Requeue with incremented retries
            await channel.default_exchange.publish(
                aio_pika.Message(body=json.dumps({
                    "id": notif_id,
                    "user_id": user_id,
                    "notif_type": notif_type,
                    "content": content,
                    "retries": retries + 1
                }).encode()),
                routing_key="notifications"
            )
        else:
            print(f"Notification {notif_id} failed after {MAX_RETRIES} retries.")
            notif.status = "failed"
    db.commit()
    db.close()

async def main():
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    channel = await connection.channel()
    queue = await channel.declare_queue("notifications", durable=True)
    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                await process_notification(message.body)

if __name__ == "__main__":
    asyncio.run(main())
