FROM python:3.11-slim

# Install poetry
RUN pip install --no-cache-dir poetry==1.8.3

WORKDIR /app

# Copy only dependency files first to leverage Docker layer caching
COPY pyproject.toml poetry.lock* ./

# Install runtime dependencies (no dev dependencies, no virtualenv inside container)
RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi

# Copy application source
COPY app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
