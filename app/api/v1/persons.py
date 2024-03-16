from fastapi import APIRouter, Depends, Path, Query

from app import models, services

router = APIRouter()


@router.get(
    "/{person_id}",
    summary="Получить полную информацию по персоне",
    response_model=models.Person,
)
async def person_details(
    person_id: str = Path(description="ID записи"),
    person_service=Depends(services.get_person_service),
) -> models.Person:
    return await person_service.get_by_id(_id=person_id)


@router.get(
    "",
    summary="Получить персоны",
    response_model=list[models.Person],
)
async def persons_details(
    sort: str | None = Query(
        pattern="^-?[^-]+$",
        default="full_name",
        description="Поле сортировки",
    ),
    page_number: int | None = Query(default=1, ge=1, description="Номер страницы"),
    page_size: int | None = Query(
        default=20,
        ge=5,
        le=50,
        description="Количество записей на странице",
    ),
    person_service=Depends(services.get_person_service),
) -> list[models.Person]:
    return await person_service.get_persons(
        sort=sort,
        page_number=page_number,
        page_size=page_size,
    )


@router.get(
    "/search/",
    summary="Получить персоны",
    response_model=list[models.Person],
)
async def persons_details_by_search(
    query: str = Query(description="Строка для поиска"),
    sort: str | None = Query(
        pattern="^-?[^-]+$",
        default="full_name",
        description="Поле сортировки",
    ),
    page_number: int | None = Query(default=1, ge=1, description="Номер страницы"),
    page_size: int | None = Query(
        default=20,
        ge=5,
        le=50,
        description="Количество записей на странице",
    ),
    person_service=Depends(services.get_person_service),
) -> list[models.Person]:
    return await person_service.get_many_by_search(
        query=query,
        sort=sort,
        page_number=page_number,
        page_size=page_size,
    )
