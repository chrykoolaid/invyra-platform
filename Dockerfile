FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src

COPY pyproject.toml README.md /app/
COPY src /app/src

RUN python -m pip install --upgrade pip \
    && python -m pip install -e ".[dev]"

EXPOSE 8000

CMD ["uvicorn", "invyra_platform.main:app", "--host", "0.0.0.0", "--port", "8000"]
