import asyncio
#mock functions for sending email, SMS, and in-app notifications
async def send_email(user_id, content):
    print(f"[MOCK EMAIL] To: {user_id} | Content: {content}") #working to be implemented to send actual mail to user using Mailgun, Gmail SMTP, etc.
    await asyncio.sleep(1)  # Simulate delay

async def send_sms(user_id, content):
    print(f"[MOCK SMS] To: {user_id} | Content: {content}") #working to be implemented to send actual SMS to user using twilo, etc
    await asyncio.sleep(1)

async def send_in_app(user_id, content):
    print(f"[IN-APP] To: {user_id} | Content: {content}") #in-app notification sent to frontend from backend
    await asyncio.sleep(1)
