import json
import secrets

from pydantic import BaseSettings

from fastapi_blog import CONFIG_PATH


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    ALGORITHM: str = "HS256"

    PROJECT_NAME: str

    @classmethod
    def from_json(cls, json_config_path):
        stng = cls()
        with open(json_config_path, "r") as f:
            config = json.load(f)
        for key, value in config.items():
            setattr(stng, key.upper(), value)
        return stng


settings = Settings.from_json(CONFIG_PATH)
