FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

RUN pip install poetry==1.8.* && poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-root --only main

COPY . .
RUN poetry install --only main

EXPOSE 8000

CMD ["uvicorn", "src.config.app:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]
