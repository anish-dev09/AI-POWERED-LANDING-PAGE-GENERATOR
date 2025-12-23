"""
CRUD operations package.
"""
from .business import (
    create_business,
    get_business,
    get_businesses,
    update_business,
    delete_business,
    get_business_count,
    business_exists
)
from .landing_page import (
    create_landing_page,
    get_landing_page,
    get_landing_pages,
    update_landing_page,
    delete_landing_page,
    publish_landing_page,
    unpublish_landing_page,
    increment_view_count,
    get_landing_page_count
)

__all__ = [
    # Business CRUD
    "create_business",
    "get_business",
    "get_businesses",
    "update_business",
    "delete_business",
    "get_business_count",
    "business_exists",
    # Landing Page CRUD
    "create_landing_page",
    "get_landing_page",
    "get_landing_pages",
    "update_landing_page",
    "delete_landing_page",
    "publish_landing_page",
    "unpublish_landing_page",
    "increment_view_count",
    "get_landing_page_count",
]