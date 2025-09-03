from typing import TYPE_CHECKING

from core.config import settings
from repos import MasterRepo
from fs.appointments.brokers import rabbit_broker, rabbit_exchange
from redis_tools.client import redis_client
from .schemas import AppointmentNotificationPub, AppointmentPayload

if TYPE_CHECKING:
    from schemas.appointments import AppointmentCreate
    from db.models import Appointment


async def process_appointment_create(
    repo: MasterRepo, appointment_in: "AppointmentCreate", idempotency_key: str
) -> "Appointment":
    appointment = await repo.appointment.create(appointment_in)
    await redis_client.set(idempotency_key, value=appointment.id)
    payload = AppointmentPayload.model_validate(appointment, from_attributes=True)
    appointment_pub = AppointmentNotificationPub(
        occurred_at=appointment.created_at,
        event_type="AppointmentCreated",
        payload=payload,
    )
    await rabbit_broker.publish(
        message=appointment_pub.model_dump(),
        queue=settings.rabbit.routing_key,
        exchange=rabbit_exchange,
    )
    return appointment
