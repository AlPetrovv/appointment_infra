from faststream.rabbit import RabbitExchange, ExchangeType

from core.config import settings

rabbit_appointment_exchange = RabbitExchange(settings.rabbit.appointment.exchange_name, type=ExchangeType.TOPIC)
notification_exchange = RabbitExchange(settings.rabbit.notification.exchange_name, type=ExchangeType.TOPIC)