import asyncio
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from src.common.settings.config import ProjectSettings
from src.infra.db.postgres.models.base import Base
from src.logic.container import init_container
from src.logic.use_case.product_category import ParseAndCreateProductCategoryUseCase


"""

Заполнив базу тестовыми данными, тесты перестанут работать и нужно будет её почистить 
TRUNCATE TABLE products, categories RESTART IDENTITY CASCADE
commit;

"""


@asynccontextmanager
async def db_engine(url) -> AsyncEngine:
    engine = create_async_engine(url, echo=True)
    try:
        yield engine
    finally:
        await engine.dispose()


async def make_migrations():
    sql_url = init_container().resolve(ProjectSettings).get_sql_db_url

    async with db_engine(sql_url) as engine:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


async def fill_db():
    await make_migrations()
    create_product_category_usecase: ParseAndCreateProductCategoryUseCase = (
        init_container().resolve(ParseAndCreateProductCategoryUseCase)
    )
    file = open("fill_test_db.xml", mode="r", encoding="utf-8")
    try:
        file_content = file.read()
        await create_product_category_usecase.parse_and_create(lxml_data=file_content)
    except Exception as e:
        raise e
    finally:
        file.close()


async def main():
    return await fill_db()


if __name__ == "__main__":
    asyncio.run(main())
