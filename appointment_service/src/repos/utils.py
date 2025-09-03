from db.manager import db_manager
from .master import MasterRepo


async def get_repo() -> MasterRepo:
    async with db_manager.session() as session:
        yield MasterRepo(session)
