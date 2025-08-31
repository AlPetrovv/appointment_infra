from typing import Annotated
from fastapi import Depends

from repos import MasterRepo
from repos import get_repo

RepoDep = Annotated[MasterRepo, Depends(get_repo)]