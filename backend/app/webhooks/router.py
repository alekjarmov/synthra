import os
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.auth.service import create_user, get_user_by_username
from app.database import get_async_session
from app.auth.models import User
from app.file_transfer.schemas import MetadataFileResponse
from app.file_transfer.service import get_all_files_user, get_file_by_id
from app.webhooks.models import Webhook
from app.webhooks.schemas import CreateWebhook
from app.webhooks.service import (
    create_webhook,
    send_webhook_file,
    get_webhook_by_id,
    get_all_webhooks_for_user,
    delete_webhook,
)

router = APIRouter(tags=["webhooks"])

WEBHOOK_URL = os.getenv(
    "WEBHOOK_EXAMPLE_URL", "Enter the webhook url here to test the webhook functionality."
)


# /webhooks/..
@router.get("/create-test-webhook", response_model=str)
async def test(session: Annotated[AsyncSession, Depends(get_async_session)]) -> str:
    user: User = await create_user("a", "a", 30, session)
    webhook: CreateWebhook = CreateWebhook(url=WEBHOOK_URL, user_id=user.id, platform="discord")
    try:
        await create_webhook(webhook, session)
    except Exception:
        print("error creating webhook")

    return "Created webhook and user"


@router.get("/send-test-webhook", response_model=str)
async def send_webhook(
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> str:
    async with session:
        user: User | None = await get_user_by_username("a", session)
        if user is None:
            return "User not found"

        user_files = await get_all_files_user(user, session)
        dog_image: MetadataFileResponse = user_files[0]
        user_webhook = user.webhooks[0]
        await send_webhook_file(user_webhook, dog_image)
    return "Sent webhook with file"


@router.post("/create", response_model=Webhook)
async def create_webhook_route(
    webhook: CreateWebhook,
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> Webhook:
    return await create_webhook(webhook, session)


@router.post("/send", response_model=str)
async def send_webhook_route(
    webhook_id: uuid.UUID,
    file_id: uuid.UUID,
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> str:
    webhook = await get_webhook_by_id(webhook_id, session)
    if webhook is None:
        raise HTTPException(status_code=404, detail="Webhook not found")

    file_data = await get_file_by_id(file_id, session)
    if file_data is None:
        raise HTTPException(status_code=404, detail="File not found")

    await send_webhook_file(webhook, file_data)
    return "Sent webhook with file"


@router.get("/user-webhooks", response_model=list[Webhook])
async def get_user_webhooks(
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> list:
    return await get_all_webhooks_for_user(current_user.id, session)


@router.delete("/delete/{webhook_id}", response_model=str)
async def delete(
    webhook_id: uuid.UUID,
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> str:
    await delete_webhook(webhook_id, session)
    return "Webhook deleted"