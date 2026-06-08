FROM python:3.11-slim

# Security best practice - non root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

# Change ownership to non-root user
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 5000

CMD ["python", "app.py"]
