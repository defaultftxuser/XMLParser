from functools import lru_cache

import redis
from punq import Container, Scope
from redis import Redis

from src.common.settings.config import ProjectSettings, get_settings
from src.common.settings.config_dev import DevProjectSettings, get_dev_settings
from src.infra.celery.redis import RedisClient
from src.infra.db.mongo.db import AsyncMongoClient
from src.infra.db.postgres.db import AsyncPostgresClient
from src.infra.db.postgres.models.lxml_models import Product, Category
from src.infra.repository.mongo.gpt_answers_repo import GPTAnswersRepo
from src.infra.repository.postgres.lxml_repos import (
    ProductRepository,
    CategoryRepository,
    ProductCategoryRepository,
)
from src.infra.repository.postgres.raw_sql import QueryRepository
from src.logic.other.gpt_service import QuerySQLService
from src.logic.other.http_client import get_http_client, HttpClient
from src.logic.repo_service.category_service import CategoryService
from src.logic.repo_service.mongo_service import MongoService
from src.logic.repo_service.product_category_service import ProductCategoryService
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

    container.register(ProjectSettings, factory=get_settings, scope=Scope.singleton)
    container.register(
        DevProjectSettings, factory=get_dev_settings, scope=Scope.singleton
    )
    settings: ProjectSettings = container.resolve(ProjectSettings)

    container.register(
        AsyncPostgresClient,
        instance=AsyncPostgresClient(settings=settings),
        scope=Scope.singleton,
    )

    async_postgres_client: AsyncPostgresClient = container.resolve(AsyncPostgresClient)

    container.register(
        ProductRepository,
        instance=ProductRepository(model=Product),
        scope=Scope.singleton,
    )

    container.register(
        CategoryRepository,
        factory=lambda: CategoryRepository(model=Category),
        scope=Scope.singleton,
    )

    container.register(
        QueryRepository,
        factory=lambda: QueryRepository(product_model=Product, category_model=Category),
    )

    query_repo = container.resolve(QueryRepository)
    product_repo = container.resolve(ProductRepository)
    category_repo = container.resolve(CategoryRepository)

    container.register(
        ProductCategoryRepository,
        factory=lambda: ProductCategoryRepository(
            product_repository=product_repo, category_repository=category_repo
        ),
        scope=Scope.singleton,
    )

    product_category_repo = container.resolve(ProductCategoryRepository)

    container.register(
        AsyncMongoClient,
        factory=lambda: AsyncMongoClient(
            settings=settings, collection=settings.mongo_collection
        ),
    )
    mongo_client = container.resolve(AsyncMongoClient)

    container.register(
        GPTAnswersRepo,
        factory=lambda: GPTAnswersRepo(client=mongo_client),
        scope=Scope.singleton,
    )
    mongo_answers_repo = container.resolve(GPTAnswersRepo)

    container.register(
        MongoService,
        instance=MongoService(repo=mongo_answers_repo),
        scope=Scope.singleton,
    )
    mongo_gpt_service = container.resolve(MongoService)

    container.register(
        QuerySQLService,
        instance=QuerySQLService(
            repository=query_repo, session=async_postgres_client.get_async_session
        ),
        scope=Scope.singleton,
    )

    container.register(LXMLParser, factory=lambda: LXMLParser, scope=Scope.singleton)
    container.register(HttpClient, factory=get_http_client)

    query_sql_service = container.resolve(QuerySQLService)
    lxml_parse = container.resolve(LXMLParser)
    httpx_client: HttpClient = container.resolve(HttpClient)

    container.register(
        CategoryService,
        instance=CategoryService(
            repository=category_repo, session=async_postgres_client.get_async_session
        ),
    )
    container.register(
        ProductService,
        instance=ProductService(
            repository=product_repo, session=async_postgres_client.get_async_session
        ),
    )
    container.register(
        ProductCategoryService,
        instance=ProductCategoryService(
            repository=product_category_repo,
            session=async_postgres_client.get_async_session,
        ),
    )
    product_category_service = container.resolve(ProductCategoryService)

    container.register(
        GPTUseCase,
        instance=GPTUseCase(
            settings=settings,
            service=query_sql_service,
            http_client=httpx_client,
            mongo_service=mongo_gpt_service,
        ),
    )

    container.register(
        ProductUseCase, instance=ProductUseCase(repository=product_category_repo)
    )

    container.register(
        CreateProductCategoryUseCase,
        instance=CreateProductCategoryUseCase(
            service=product_category_service,
        ),
    )
    product_service_usecase = container.resolve(CreateProductCategoryUseCase)

    container.register(
        ParseAndCreateProductCategoryUseCase,
        instance=ParseAndCreateProductCategoryUseCase(
            parser=lxml_parse,
            product_service_usecase=product_service_usecase,
        ),
    )

    def resolve_redis() -> Redis:
        return redis.Redis(host=settings.redis_host, port=settings.redis_port)

    container.register(RedisClient, factory=resolve_redis, scope=Scope.singleton)

    return container
