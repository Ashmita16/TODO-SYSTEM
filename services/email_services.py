import json
import io
from fastapi import UploadFile
from fastapi_mail import (
    FastMail,
    MessageSchema,
    ConnectionConfig,
    MessageType
)

from new.email import email_settings

mail_config = ConnectionConfig(
    MAIL_USERNAME=email_settings.MAIL_USERNAME,
    MAIL_PASSWORD=email_settings.MAIL_PASSWORD,
    MAIL_FROM=email_settings.MAIL_FROM,
    MAIL_FROM_NAME=email_settings.MAIL_FROM_NAME,
    MAIL_PORT=email_settings.MAIL_PORT,
    MAIL_SERVER=email_settings.MAIL_SERVER,
    MAIL_STARTTLS=email_settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=email_settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)


def format_datetime(value):
    if value is None:
        return None
    return value.strftime("%Y-%m-%d %H:%M:%S")


def create_todo_json(todos):
    todo_data = []
    for todo in todos:
        todo_data.append({
            "id": todo.id,
            "title": todo.title,
            "description": todo.description,
            "is_completed": todo.is_completed,
            "category_id": todo.category_id,
            "created_at": format_datetime(todo.created_at),
            "updated_at": format_datetime(todo.updated_at)
        })
    return json.dumps(todo_data, indent=4)



async def send_welcome_email(recipient_email: str, username: str):
    print(f"SENDING WELCOME EMAIL TO: {recipient_email}")
    
    message = MessageSchema(
        subject="WELCOME TO TODO MANAGEMENT SYSTEM",
        recipients=[recipient_email],
        body=f"""
Hello {username},

WELCOME TO THE TODO MANAGEMENT SYSTEM!

Your account has been successfully created.

You now have a simple space to organize your tasks, manage categories, track your progress, and keep your day on track.

Whether it's something you need to finish today or a goal you're working towards, we've got your todos covered.

It's time to turn your plans into action.

BEST REGARDS,
YOURS TODO
""",
        subtype=MessageType.plain
    )

    try:
        fast_mail = FastMail(mail_config)
        await fast_mail.send_message(message)
        print("WELCOME EMAIL DELIVERED!")
    except Exception as e:
        print(f"FAILED TO SEND WELCOME EAMIL: {e}")

async def send_todos_email(recipient_email: str, username: str, todos: list):
    print(f"EXPORTING TODOS EMAIL FOR: {recipient_email}")
    json_data = create_todo_json(todos)

    json_bytes = io.BytesIO(json_data.encode("utf-8"))
    attachment_file = UploadFile(
        filename="todos.json",
        file=json_bytes,
        headers={"content-type": "application/json"}
    )

    message = MessageSchema(
        subject="Your TODO List - TODO MANAGEMENT SYSTEM",
        recipients=[recipient_email],
        body=f"""
Hello {username},

Here's your TODO snapshot!

Attached to this email, you'll find your current Todo list from the TODO MANAGEMENT SYSTEM.

The attached `todos.json` file contains all the tasks you've created, along with their details, so you can keep a convenient copy of your tasks whenever you need it.

Plan it. Track it. Get it done. 
Happy organizing!

BEST REGARDS,
YOURS TODO

""",
        subtype=MessageType.plain,
        attachments=[attachment_file]
    )

    try:
        fast_mail = FastMail(mail_config)
        await fast_mail.send_message(message)
        print("TODOS DELIVERED!")
    except Exception as e:
        print(f"FALIED TO SEND TODOS: {e}")
