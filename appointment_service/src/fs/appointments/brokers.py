from faststream.rabbit import RabbitBroker, RabbitExchange, ExchangeType

from core.config import settings

__all__ = ("rabbit_broker", "rabbit_exchange")
rabbit_broker = RabbitBroker(str(settings.rabbit.url))
rabbit_exchange = RabbitExchange(settings.rabbit.exchange_name, type=ExchangeType.TOPIC)
