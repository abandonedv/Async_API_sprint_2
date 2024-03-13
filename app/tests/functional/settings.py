from pydantic_settings import BaseSettings, SettingsConfigDict


class ElasticParams(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="ELASTIC_", env_file=".env.test")

    host: str
    port: int

    def url(self):
        return f"http://{self.host}:{self.port}"


class RedisParams(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="REDIS_", env_file=".env.test")

    host: str
    port: int

    def url(self):
        return f"{self.host}:{self.port}"
