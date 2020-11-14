# fastapi-blog
FastApi App for Web Blogging

Project uses Poetry for dependency management and packaging.
To install dependencies run:
```bash
    poetry install
```

To start an app run:
```bash
    uvicorn fastapi_blog.app:app --reload --port 8080
```

## Using Docker to run an App
To run an app, you need to build Docker first by typing simple command:
```
docker build . -t fastapi-blog 
```
Then you can run an app in the container:
```
docker run -it --rm -p 8080:8080 fastapi-blog:latest
```
Now you can access the app at http://localhost:8080/

## Development
Project uses pre-commit hooks for development, to set them up run:
```bash
    pre-commit install
```
to install git hooks in your .git/ directory.