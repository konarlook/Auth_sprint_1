from fastapi import APIRouter

router = APIRouter()


@router.post("/roles/create", tags=["roles"])
async def create_role():
    pass


@router.get("/roles/read", tags=["roles"])
async def get_roles():
    pass


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
