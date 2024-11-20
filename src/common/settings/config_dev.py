from dotenv import load_dotenv, find_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv(find_dotenv(".env.dev"))


class DevProjectSettings(BaseSettings):

    postgres_database: str = Field(alias="SQL_DATABASE")
    postgres_engine: str = Field(alias="SQL_ENGINE")
    postgres_user: str = Field(alias="POSTGRES_USER")
    postgres_password: str = Field(alias="POSTGRES_PASSWORD")
    postgres_host: str = Field(alias="POSTGRES_HOST")
    postgres_port: str = Field(alias="POSTGRES_PORT")
    postgres_name: str = Field(alias="POSTGRES_NAME")

    mongo_database: str = Field(alias="NO_SQL_DATABASE")
    mongo_user: str = Field(alias="MONGO_INITDB_ROOT_USERNAME")
    mongo_password: str = Field(alias="MONGO_INITDB_ROOT_PASSWORD")
    mongo_host: str = Field(alias="MONGO_INITDB_ROOT_HOST")
    mongo_port: str = Field(alias="MONGO_INITDB_PORT")
    mongo_collection: str = Field(alias="MONGO_INITDB_DATABASE")

    broker: str = Field(alias="BROKER")
    redis_host: str = Field(alias="REDIS_HOST")
    redis_port: str = Field(alias="REDIS_PORT")

    celery_name: str = Field("CELERY_NAME")

    @property
    def get_sql_db_url(self) -> str:
        return "{}+{}://{}:{}@{}:{}/{}".format(
            self.postgres_database,
            self.postgres_engine,
            self.postgres_user,
            self.postgres_password,
            self.postgres_host,
            self.postgres_port,
            self.postgres_name,
        )

    @property
    def get_no_sql_db_url(self) -> str:
        return "{}://{}:{}@{}:{}".format(
            self.mongo_database,
            self.mongo_database,
            self.mongo_user,
            self.mongo_password,
            self.mongo_host,
            self.mongo_port,
        )

    @property
    def get_redis_url(self) -> str:
        return "{}://:@{}:{}/0".format(
            self.broker,
            self.redis_host,
            self.redis_port,
        )


def get_settings() -> DevProjectSettings:
    return DevProjectSettings()
