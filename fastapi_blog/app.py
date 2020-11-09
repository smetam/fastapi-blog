import uvicorn
from fastapi import FastAPI
from pydantic import BaseSettings


class Settings(BaseSettings):
    message: str


settings = Settings()
app = FastAPI()


@app.get("/settings")
def get_settings():
    return {"message": settings.message}


if __name__ == "__main__":
    uvicorn.run("fastapi_code:app")
