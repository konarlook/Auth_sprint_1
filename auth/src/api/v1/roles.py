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


@router.post("/roles/delete", tags=["roles"])
async def delete_role():
    pass


@router.post("/roles/set", tags=["roles"])
async def search_role():
    pass


@router.post("/roles/deprive", tags=["roles"])
async def deprive_role():
    pass


@router.post("/roles/grant", tags=["roles"])
async def grant_role():
    pass


@router.post("/roles/verify", tags=["roles"])
async def verify_role():
    pass
