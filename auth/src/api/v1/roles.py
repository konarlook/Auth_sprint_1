import uuid
from http import HTTPStatus
from http.client import HTTPException

from fastapi import APIRouter, Depends

from schemas.roles import RolesActionsSchema
from services.role import RoleService, get_role_service

router = APIRouter()


@router.post("/roles/create", tags=["roles"])
async def create_role():
    pass


@router.get(path="/roles/read", response_model=list[RolesActionsSchema], tags=["roles"])
async def get_roles(role_service: RoleService = Depends(get_role_service)):
    response = await role_service.get_all_roles()
    if not response:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="roles not found")
    return response


@router.post("/roles/update", tags=["roles"])
async def update_role():
    pass


@router.post("/roles/delete/{name}", tags=["roles"])
async def delete_role(name: str, role_service: RoleService = Depends(get_role_service)):
    response = await role_service.delete_role(name=name)
    if not response:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="role not found")
    return HTTPStatus.OK


@router.post("/roles/set", tags=["roles"])
async def set_role(
    user_id: uuid.UUID,
    role_name: str,
    role_service: RoleService = Depends(get_role_service),
):
    # TODO(Mosyagingrigorii): Доабвить проверку на существование пользователя
    role_data = await role_service.is_exist_role(name=role_name)
    if not role_data:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="role not found")
    await role_service.set_role(user_id=user_id, role_name=role_name)
    return HTTPStatus.OK


@router.post("/roles/deprive", tags=["roles"])
async def deprive_role():
    pass


@router.post("/roles/grant", tags=["roles"])
async def grant_role():
    pass


@router.post("/roles/verify", tags=["roles"])
async def verify_role():
    pass
