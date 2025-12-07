from typing import Annotated

from fastapi import Depends

from services.auth_service import current_user_id

#
# def current_user(
#         request: Request,
#         auth_service: AuthService = Depends(get_auth_service),
# ) -> str:
#     token = request.headers.get("Authorization")  # 👈 name must match set_cookie key
#     print(token)
#
#     if not token:
#         print('Not Token')
#         try:
#             return current_user_service()
#         except Exception:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Not authenticated",
#             )
#
#     try:
#         return auth_service.get_current_user(token)
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail=str(e),
#         )


user_dep = Annotated[str, Depends(current_user_id)]
