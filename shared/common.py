from typing import Annotated

from fastapi import Depends, HTTPException, Request, status

from user_service.services.auth_service import AuthService, get_auth_service
from user_service.services.auth_service import current_user_id as current_user_service


def current_user(
        request: Request,
        auth_service: AuthService = Depends(get_auth_service),
) -> str:
    token = request.cookies.get("jwt")  # 👈 name must match set_cookie key

    if not token:
        try:
            return current_user_service()
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
            )

    try:
        return auth_service.get_current_user(token)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )


user_dep = Annotated[str, Depends(current_user)]
