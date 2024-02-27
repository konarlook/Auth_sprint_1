import uuid

from fastapi import APIRouter, Depends, status, HTTPException

from schemas.roles import RolesActionsSchema, CreateRoleSchema
from services.role import RoleService, get_role_service

router = APIRouter()


@router.post(
    "/roles/create",
    response_model=CreateRoleSchema,
    status_code=status.HTTP_201_CREATED,
    tags=["roles"],
    description="Создать роль на основании имеющихся возможных действий",
    summary="Создать роль",
)
async def create_role(
    query_params: CreateRoleSchema = Depends(),
    role_service: RoleService = Depends(get_role_service),
) -> CreateRoleSchema:
    # TODO(Mosyagingrigorii): Подумать над обработкой исключений
    db_obj = await role_service.create_role(query_params)
    return db_obj


@router.get(
    path="/roles/read",
    response_model=list[RolesActionsSchema],
    status_code=status.HTTP_200_OK,
    tags=["roles"],
    description="Получить существующие роли с детализацией по разрешенным действиям",
    summary="Получить существующие роли",
)
async def get_roles(
    role_service: RoleService = Depends(get_role_service),
) -> list[RolesActionsSchema]:
    response = await role_service.get_all_roles()
    if not response:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT, detail="roles not found"
        )
    return response


@router.put(
    "/roles/update",
    response_model=CreateRoleSchema,
    status_code=status.HTTP_200_OK,
    tags=["roles"],
    description="Изменить название, комментарий и разрешенные действия у существующей роли",
    summary="Изменить существующую роль",
)
async def update_role(
    query_params: CreateRoleSchema = Depends(),
    role_service: RoleService = Depends(get_role_service),
) -> CreateRoleSchema:
    db_obj = await role_service.update_role(query_params)
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="roles not found"
        )
    return db_obj


@router.delete(
    "/roles/delete/{name}",
    status_code=status.HTTP_200_OK,
    tags=["roles"],
    description="Изменить название, комментарий и разрешенные действия у существующей роли",
    summary="Изменить существующую роль",
)
async def delete_role(name: str, role_service: RoleService = Depends(get_role_service)):
    response = await role_service.delete_role(name=name)
    if not response:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="role not found"
        )
    return


@router.post(
    "/roles/set",
    status_code=status.HTTP_201_CREATED,
    tags=["roles"],
    description="Назначить роль пользователю",
    summary="Назначить роль пользователю",
)
async def set_role(
    user_id: uuid.UUID,
    role_name: str,
    role_service: RoleService = Depends(get_role_service),
):
    # TODO(Mosyagingrigorii): Доабвить проверку на существование пользователя
    role_data = await role_service.is_exist_role(name=role_name)
    if not role_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="role not found"
        )
    await role_service.set_role(user_id=user_id, role_name=role_name)
    return


@router.post(
    "/roles/verify",
    status_code=status.HTTP_200_OK,
    tags=["roles"],
    description="Верифицировать роль пользователя",
    summary="Верифицировать роль пользователя",
)
async def verify_role(
    user_id: uuid.UUID,
    role_name: str,
    role_service: RoleService = Depends(get_role_service),
):
    is_verified = await role_service.verify_role(user_id=user_id, role_name=role_name)
    if not is_verified:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="role isn't verified"
        )
    return
