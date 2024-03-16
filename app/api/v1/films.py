from fastapi import APIRouter, Depends, Path, Query

from app import models, services

router = APIRouter()


@router.get(
    "/{film_id}",
    summary="Получить полную информацию по фильму",
    response_model=models.Film,
)
async def film_details(
    film_id: str = Path(description="ID записи"),
    film_service=Depends(services.get_film_service),
) -> models.Film:
    return await film_service.get_by_id(_id=film_id)


@router.get(
    "",
    summary="Получить фильмы",
    response_model=list[models.Film],
)
async def films_details(
    sort: str | None = Query(pattern="^-?[^-]+$", default="-imdb_rating"),
    genre: str | None = Query(default=None, description="Название жанра"),
    actor: str | None = Query(default=None, description="Полное имя актера"),
    writer: str | None = Query(default=None, description="Полное имя сценариста"),
    page_number: int | None = Query(default=1, ge=1, description="Номер страницы"),
    page_size: int | None = Query(
        default=20,
        ge=5,
        le=50,
        description="Количество записей на странице",
    ),
    film_service=Depends(services.film.get_film_service),
) -> list[models.Film]:
    return await film_service.get_films(
        sort=sort,
        genre=genre,
        actor=actor,
        writer=writer,
        page_number=page_number,
        page_size=page_size,
    )


@router.get(
    "/search/",
    summary="Получить фильмы",
    response_model=list[models.Film],
)
async def films_details_by_search(
    query: str = Query(description="Строка для поиска"),
    sort: str | None = Query(
        pattern="^-?[^-]+$",
        default="-imdb_rating",
        description="Поле сортировки",
    ),
    page_number: int | None = Query(default=1, ge=1, description="Номер страницы"),
    page_size: int | None = Query(
        default=20,
        ge=5,
        le=50,
        description="Количество записей на странице",
    ),
    film_service=Depends(services.film.get_film_service),
) -> list[models.Film]:
    return await film_service.get_many_by_search(
        query=query,
        sort=sort,
        page_number=page_number,
        page_size=page_size,
    )
