import pytest

from app.city.schema import CitySchemaRead
from app.food.schemas import (
    CategorySchemaRead,
    FoodSchemaRead,
    ShopSchemaRead,
)

GENERATING_RANGE = range(10, 20)


@pytest.fixture
def get_city_list():
    return [CitySchemaRead(id=cnt, name=f"city-test-{cnt}") for cnt in GENERATING_RANGE]


@pytest.fixture
def get_shop_list():
    return [
        ShopSchemaRead(id=cnt, name=f"city-test-{cnt}", rate=0.0 + cnt, city=cnt)
        for cnt in GENERATING_RANGE
    ]


@pytest.fixture
def get_category_list():
    return [
        CategorySchemaRead(id=cnt, name=f"category-test-{cnt}")
        for cnt in GENERATING_RANGE
    ]


@pytest.fixture
def get_food_list():
    return [
        FoodSchemaRead(
            id=cnt,
            name=f"food-test-{cnt}",
            rate=0.0 + cnt,
            description="test",
            price=cnt,
            shop=cnt,
            category=cnt,
        )
        for cnt in GENERATING_RANGE
    ]
