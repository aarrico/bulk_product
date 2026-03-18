FROM python:3.14-slim

WORKDIR /app

# Install deps first for better layer caching
COPY pyproject.toml .
RUN mkdir -p app && touch app/__init__.py && pip install --no-cache-dir .

# Copy real source and install package in editable mode
COPY . .
RUN pip install --no-cache-dir -e .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
