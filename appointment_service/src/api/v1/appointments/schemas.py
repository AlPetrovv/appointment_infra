from pydantic import BaseModel


class IdempotencyHeaders(BaseModel):
    idempotency_key: str