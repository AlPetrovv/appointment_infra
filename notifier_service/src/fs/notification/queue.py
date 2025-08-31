
from faststream.rabbit import RabbitQueue

from core.config import settings

appointment_created_queue = RabbitQueue("appointment-created", routing_key=settings.rabbit.appointment.routing_key)
