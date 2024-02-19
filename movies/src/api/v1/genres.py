from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from services.genre import GenreService, get_genre_service
from models.models import Genre, Page
from models.request_models import BaseModelPaginationFilter

router = APIRouter()


# TODO(MosyaginGrigorii): Возможно, имеет смысл добавить фильтрацию
@router.get(
    "/genres/",
    response_model=Page[Genre],
    summary="Информация о жанрах",
    description="Информация о жанрах",
    response_description="Список жанров",
    tags=["Главная страница"],
)
async def genres_list(
    query_params: BaseModelPaginationFilter = Depends(),
    genre_service: GenreService = Depends(get_genre_service),
) -> Page[Genre] | None:
    response_genres = await genre_service.get_list_genres(
        query_params.page_size, query_params.page_number
    )
    if not response_genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="genres not found")

    return response_genres


@router.get(
    "/genres/{genre_id}",
    response_model=Genre,
    summary="Информация о жанре",
    description="Информация о жанре",
    response_description="Жанр",
    tags=["Страница жанра"],
)
async def get_genre_bu_id(
    genre_id: UUID,
    genre_service: GenreService = Depends(get_genre_service),
) -> Genre:
    response_genre = await genre_service.get_by_id(entity_id=genre_id)
    if not response_genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="genre not found")
    return response_genre
