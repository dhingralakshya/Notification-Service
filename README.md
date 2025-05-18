# Notification Service Backend

## Overview

A scalable backend notification service built with FastAPI, SQLAlchemy, and RabbitMQ.  
It supports sending email, SMS, and in-app notifications (mocked for demo/safety), with robust queue-based background processing and retry logic.

---

## Features

- RESTful API endpoints to send and fetch notifications
- Supports email, SMS, and in-app notification types
- Asynchronous background worker for processing notifications
- Retry mechanism for failed notifications (up to 3 attempts)
- SQLite database for persistence (easy to swap for MySQL/MongoDB)
- Clear, modular project structure and code

---

## Technologies Used

- Python
- FastAPI
- SQLAlchemy
- aio_pika (RabbitMQ integration)
- Pydantic
- SQLite
- Docker (for RabbitMQ)

---

## Setup Instructions

### 1. Clone the Repository
    git clone https://github.com/dhingralakshya/Notification-Service.git
    cd notification_service
    
### 2. Install Dependencies
    pip install -r requirements.txt

### 3. Start RabbitMQ (with Docker)
    docker run -d --hostname my-rabbit --name some-rabbit -p 5672:5672 rabbitmq:3

### 4. Start the FastAPI Server(by going inside app directory)
    cd app
    uvicorn main:app --reload

### 5. Start the Worker (in a new terminal, also ensure being inside the app directory)
    python -m app.worker


## API Usage

### Send a Notification

**POST** `/notifications/`
**Body Example:**
{
"user_id": "user123",
"notif_type": "email", // or "sms" or "in_app"
"content": "Welcome to the platform!"
}

### Get User Notifications

**GET** `/users/{user_id}/notifications`


## How It Works

- The API receives notification requests and stores them as "pending".
- Each notification is published to a RabbitMQ queue.
- A background worker consumes the queue, processes notifications (mocked sending), and updates their status to "sent" or "failed" after up to 3 retries.
- All notifications are stored and can be fetched via the API.


## Mock vs. Real Notifications

- **Email/SMS sending is mocked** for demo purposes.
- To use real services (e.g., Mailgun, Twilio), update `app/services.py` with your provider’s integration.
