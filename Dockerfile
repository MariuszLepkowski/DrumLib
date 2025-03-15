FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    graphviz \
    libgraphviz-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY DrumLib/. /app/

ENV PYTHONPATH=/app

RUN python manage.py collectstatic --noinput

ENTRYPOINT ["sh", "-c", "python manage.py migrate && python create_superuser.py && gunicorn --bind 0.0.0.0:$PORT DrumLib.wsgi:application"]
