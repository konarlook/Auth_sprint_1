from fastapi import APIRouter, Depends, status, Path

from schemas import roles
from services.role_service import AuthRoleService, get_role_service

router = APIRouter()


@router.post(
    "/roles/create",
    status_code=status.HTTP_201_CREATED,
    tags=["roles"],
    description="Создать роль на основании имеющихся возможных действий",
    summary="Создать роль",
)
async def create_role(
    role_dto: roles.RoleActionDto = Depends(),
    role_service: AuthRoleService = Depends(get_role_service),
):
    pass


@router.get(
    path="/roles/read",
    response_model=list[roles.RoleActionSchema],
    status_code=status.HTTP_200_OK,
    tags=["roles"],
    description="Получить существующие роли с детализацией по разрешенным действиям",
    summary="Получить существующие роли",
)
async def get_roles(
    role_service: AuthRoleService = Depends(get_role_service),
) -> list[roles.RoleActionSchema]:
    pass


@router.put(
    "/roles/update",
    status_code=status.HTTP_200_OK,
    tags=["roles"],
    description="Изменить название, комментарий и разрешенные действия у существующей роли",
    summary="Изменить существующую роль",
)
async def update_role(
    role_dto: roles.RoleActionDto = Depends(),
    role_service: AuthRoleService = Depends(get_role_service),
):
    pass


@router.delete(
    "/roles/delete/{name}",
    status_code=status.HTTP_200_OK,
    tags=["roles"],
    description="Изменить название, комментарий и разрешенные действия у существующей роли",
    summary="Изменить существующую роль",
)
async def delete_role(
    name: str = Path(max_length=50, title="Имя роли"),
    role_service: AuthRoleService = Depends(get_role_service),
):
    pass


@router.post(
    "/roles/set",
    status_code=status.HTTP_201_CREATED,
    tags=["roles"],
    description="Назначить роль пользователю",
    summary="Назначить роль пользователю",
)
async def set_role(
    user_dto: roles.UserRoleDto = Depends(),
    role_service: AuthRoleService = Depends(get_role_service),
):
    pass


@router.post(
    "/roles/verify",
    status_code=status.HTTP_200_OK,
    tags=["roles"],
    description="Верифицировать роль пользователя",
    summary="Верифицировать роль пользователя",
)
async def verify_role(
    user_dto: roles.UserRoleDto = Depends(),
    role_service: AuthRoleService = Depends(get_role_service),
):
    pass
