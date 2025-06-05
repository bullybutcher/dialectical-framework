#SETUP GUIDE

Upon cloning this repo, you have to:
- Install dependencies through Poetry
- Run server using Uvicorn

## Poetry 

### Install Poetry 

```bash
pip install poetry
```

### Install Poetry Dependencies

```bash
poetry install
```

If there is an existing `poetry.lock` file and changes have been made to `pyproject.toml`, run this:
```bash
poetry lock && poetry install
```

## Run Server

```bash
poetry run uvicorn app.main:app --port 8000
```