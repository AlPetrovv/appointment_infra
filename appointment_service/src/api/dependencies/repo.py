from typing import Annotated
from fastapi import Depends

from repos import MasterRepo, get_repo

RepoDep = Annotated[MasterRepo, Depends(get_repo)]
