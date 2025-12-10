from typing import Annotated

from fastapi import Depends

from services.auth_service import current_user_id

user_dep = Annotated[str, Depends(current_user_id)]
