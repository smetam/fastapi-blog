FROM python:3.7
WORKDIR /app
COPY poetry.lock pyproject.toml /app/
RUN pip install poetry

COPY fastapi_blog /app/fastapi_blog
RUN cd /app/fastapi_blog \
    &&  poetry install --no-dev && cd /app

EXPOSE 80

CMD ["uvicorn", "fastapi_blog.app:app", "--host", "0.0.0.0", "--port", "80"]