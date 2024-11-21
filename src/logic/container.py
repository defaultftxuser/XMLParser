from functools import lru_cache

import httpx
from punq import Container, Scope

from src.common.settings.config import ProjectSettings, get_settings
from src.infra.db.mongo.db import AsyncMongoClient
from src.infra.db.postgres.db import AsyncPostgresClient
from src.infra.db.postgres.models.lxml_models import Product, Category
from src.infra.repository.mongo.gpt_answers_repo import GPTAnswersRepo
from src.infra.repository.postgres.base_postgres import PostgresRepo
from src.infra.repository.postgres.lxml_repos import (
    ProductRepository,
    CategoryRepository,
    ProductCategoryRepository,
)
from src.infra.repository.postgres.raw_sql import QueryRepository
from src.logic.other.gpt_service import QuerySQLService
from src.logic.other.http_client import HttpClient
from src.logic.repo_service.category_service import CategoryService
from src.logic.repo_service.produce_category_service import ProductCategoryService
from src.logic.repo_service.product_service import ProductService
from src.logic.use_case.gpt_usecase import GPTUseCase
from src.logic.use_case.product_category import (
    CreateProductCategoryUseCase,
    ParseAndCreateProductCategoryUseCase,
)
from src.logic.use_case.products import ProductUseCase
from src.logic.xml_parser import LXMLParser


@lru_cache(1)
def init_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()

    # register common layer dependencies

    container.register(ProjectSettings, factory=get_settings, scope=Scope.singleton)

    settings: ProjectSettings = container.resolve(ProjectSettings)

    container.register(
        AsyncPostgresClient,
        instance=AsyncPostgresClient(settings=settings),
        scope=Scope.singleton,
    )

    async_postgres_client = container.resolve(AsyncMongoClient)

    # register infra layer dependencies

    container.register(
        PostgresRepo,
        instance=ProductRepository(model=Product),
        scope=Scope.singleton,
    )

    container.register(
        CategoryRepository,
        instance=CategoryRepository(model=Category),
        scope=Scope.singleton,
    )

    container.register(
        QueryRepository,
        instance=QueryRepository(product_model=Product, category_model=Category),
    )

    query_repo = container.resolve(QueryRepository)
    product_repo = container.resolve(ProductRepository)
    category_repo = container.resolve(CategoryRepository)

    container.register(
        ProductCategoryRepository,
        instance=ProductCategoryRepository(
            product_repository=product_repo, category_repository=category_repo
        ),
        scope=Scope.singleton,
    )

    product_category_repo = container.resolve(ProductCategoryRepository)

    container.register(
        AsyncMongoClient,
        instance=AsyncMongoClient(
            settings=settings, collection=settings.mongo_collection
        ),
    )
    mongo_client = container.resolve(AsyncMongoClient)

    container.register(GPTAnswersRepo, instance=GPTAnswersRepo(client=mongo_client))

    mongo_answers_repo = container.resolve(GPTAnswersRepo)

    container.register(
        QuerySQLService,
        instance=QuerySQLService(repository=query_repo, uow=async_postgres_client),
    )

    container.register(LXMLParser, instance=LXMLParser())

    container.register(HttpClient, instance=HttpClient(client=httpx.AsyncClient()))
    query_sql_service = container.resolve(QuerySQLService)
    lxml_parse = container.resolve(LXMLParser)
    httpx_client = container.resolve(HttpClient)

    container.register(
        CategoryService, instance=CategoryService(repository=category_repo)
    )
    container.register(ProductService, instance=ProductService(repository=product_repo))
    container.register(
        ProductCategoryService,
        instance=ProductCategoryService(repository=product_category_repo),
    )
    category_service = container.resolve(CategoryService)
    product_service = container.resolve(ProductService)

    container.register(
        GPTUseCase,
        instance=GPTUseCase(
            settings=settings,
            service=query_sql_service,
            http_client=httpx_client,
            repository=mongo_answers_repo,
        ),
    )

    container.register(
        ProductUseCase, instance=ProductUseCase(repository=product_category_repo)
    )

    container.register(
        CreateProductCategoryUseCase,
        instance=CreateProductCategoryUseCase(
            category_service=category_service,
            product_service=product_service,
            uow=async_postgres_client,
        ),
    )

    container.register(
        ParseAndCreateProductCategoryUseCase,
        instance=ParseAndCreateProductCategoryUseCase(
            category_service=category_service,
            product_service=product_service,
            uow=async_postgres_client,
            parser=lxml_parse,
        ),
    )
    return container
