from fastapi import APIRouter, Depends, Path, Query

from app import models, services

router = APIRouter()


@router.get(
    "/{genre_id}",
    summary="Получить полную информацию по жанру",
    response_model=models.Genre,
)
async def genre_details(
    genre_id: str = Path(description="ID записи"),
    genre_service=Depends(services.get_genre_service),
) -> models.Genre:
    return await genre_service.get_by_id(_id=genre_id)


@router.get(
    "",
    summary="Получить жанры",
    response_model=list[models.Genre],
)
async def genres_details(
    sort: str | None = Query(
        pattern="^-?[^-]+$",
        default="name",
        description="Поле сортировки",
    ),
    page_number: int | None = Query(default=1, ge=1, description="Номер страницы"),
    page_size: int | None = Query(
        default=20,
        ge=5,
        le=50,
        description="Количество записей на странице",
    ),
    genre_service=Depends(services.get_genre_service),
) -> list[models.Genre]:
    return await genre_service.get_genres(
        sort=sort,
        page_number=page_number,
        page_size=page_size,
    )


@router.get(
    "/search/",
    summary="Получить жанры",
    response_model=list[models.Genre],
)
async def genres_details_by_search(
    query: str = Query(description="Строка для поиска"),
    sort: str | None = Query(
        pattern="^-?[^-]+$",
        default="name",
        description="Поле сортировки",
    ),
    page_number: int | None = Query(default=1, ge=1, description="Номер страницы"),
    page_size: int | None = Query(
        default=20,
        ge=5,
        le=50,
        description="Количество записей на странице",
    ),
    genre_service=Depends(services.get_genre_service),
) -> list[models.Genre]:
    return await genre_service.get_many_by_search(
        query=query,
        sort=sort,
        page_number=page_number,
        page_size=page_size,
    )
