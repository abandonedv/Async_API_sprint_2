from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_PATH = "app/tests/functional/.env.test"


class ElasticParams(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="ELASTIC_", env_file=ENV_PATH)

    host: str
    port: int

    def url(self):
        return f"http://{self.host}:{self.port}"


class RedisParams(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="REDIS_", env_file=ENV_PATH)

    host: str
    port: int

    def url(self):
        return f"{self.host}:{self.port}"


class ServiceParams(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="SERVICE_", env_file=ENV_PATH)

    host: str
    port: int

    def url(self):
        return f"http://{self.host}:{self.port}"
