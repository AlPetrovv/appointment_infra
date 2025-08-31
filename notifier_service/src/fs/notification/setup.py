
# # from .brokers import rabbit_broker, rabbit_exchange
# from .queue import appointment_created_queue
#
# async def bind_queue_exchange():
#     queue: aio_pika.RobustQueue = await rabbit_broker.declare_queue(
#         appointment_created_queue
#     )
#
#     exchange: aio_pika.RobustExchange = await rabbit_broker.declare_exchange(
#         rabbit_exchange
#     )
#     await queue.bind(exchange=exchange)