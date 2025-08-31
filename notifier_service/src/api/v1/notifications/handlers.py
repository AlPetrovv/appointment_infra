from typing import Annotated

from faststream.rabbit.fastapi import RabbitRouter
from fastapi import APIRouter, Query
from fastapi_pagination import paginate
from pydantic_extra_types.phone_numbers import PhoneNumber

from api.dependencies.repo import RepoDep
from api.v1.pagination import CustomPage
from schemas.notifications import NotificationRead, NotificationCreate

from api.v1.notifications.schemas import AppointmentCreatedNotification

from core.config import settings
from fs.notification.queue import appointment_created_queue

from schemas.events import ProcessedEventCreate

from fs.notification.brokers import rabbit_appointment_exchange, notification_exchange

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
    responses={404: {"description": "Not found"}},
)

fs_router = RabbitRouter(str(settings.rabbit.url))


@router.get("/", status_code=200)
async def get_notifications(
        repo: RepoDep,
        customer_phone: Annotated[PhoneNumber, Query(alias="customer_phone")]
) -> CustomPage[NotificationRead]:
    notifications = await repo.notification.get_by_customer_phone(customer_phone=customer_phone)
    return paginate(notifications)


@fs_router.publisher(settings.rabbit.notification.routing_key, notification_exchange)
@fs_router.subscriber(queue=appointment_created_queue,exchange=rabbit_appointment_exchange)
async def appointment_created(appointment_notification: AppointmentCreatedNotification, repo: RepoDep) -> str | None:
    pe = await repo.processed_event.get(appointment_notification.event_id)
    if pe is not None:
        return None
    pe_in = ProcessedEventCreate(
        type=appointment_notification.event_type,
        occurred_at=appointment_notification.occurred_at)
    await repo.processed_event.create(pe_in)
    notification_in = NotificationCreate(
        appointment_data=appointment_notification.payload,
    )
    await repo.notification.create(notification_in)
    return "OK"
