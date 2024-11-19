from dotenv import load_dotenv, find_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings


load_dotenv(find_dotenv(".env"))


class ProjectSettings(BaseSettings):
    database: str = Field(alias="DATABASE")
    engine: str = Field(alias="ENGINE")
    postgres_host: str = Field(alias="POSTGRES_HOST")
    postgres_port: str = Field(alias="POSTGRES_PORT")
    postgres_user: str = Field(alias="POSTGRES_USER")
    postgres_password: str = Field(alias="POSTGRES_PASSWORD")
    postgres_name: str = Field(alias="POSTGRES_NAME")

    @property
    def get_db_url(self) -> str:
        return "{}+{}://{}:{}@{}:{}/{}".format(
            self.database,
            self.engine,
            self.postgres_user,
            self.postgres_password,
            self.postgres_host,
            self.postgres_port,
            self.postgres_name,
        )


def get_settings() -> ProjectSettings:
    return ProjectSettings()
