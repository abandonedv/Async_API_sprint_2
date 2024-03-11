def get_sort_params(sort: str) -> tuple[str, str]:
    sort_type, field_name = ("desc", sort[1:]) if sort[0] == "-" else ("asc", sort)
    return sort_type, field_name


def get_offset(page_number: int, page_size: int) -> int:
    return (page_number - 1) * page_size
