FROM python:3.10
LABEL author='Label A'

WORKDIR /app

# Environment
RUN apt-get update \
    && apt-get install -y bash vim nano postgresql-client dos2unix \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

# Major pinned python dependencies
RUN pip install --no-cache-dir flake8==3.8.4 uWSGI

# Regular Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy our codebase into the container
COPY . .

# Convert line endings to Unix format for manage.py
RUN dos2unix /app/manage.py

RUN ./manage.py collectstatic --noinput

# Ops Parameters
ENV WORKERS=2
ENV PORT=80
ENV PYTHONUNBUFFERED=1

EXPOSE ${PORT}

CMD uwsgi --http :${PORT} --processes ${WORKERS} --static-map /static=/static --module autocompany.wsgi:application
