from pydantic_settings import BaseSettings, SettingsConfigDict


class TestDBParams(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="POSTGRES_", env_file=".env.test")

    host: str
    port: int
    db: str
    user: str
    password: str

    def url(self):
        return f"{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


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
