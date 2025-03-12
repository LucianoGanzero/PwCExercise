FROM python:3.10.12-slim

RUN pip install poetry==1.8.4

RUN apt-get update && apt-get install libpq-dev gcc -y

# Set the working directory in the container
WORKDIR /app

COPY ./ ./

# Install the dependencies
RUN poetry install && rm -rf $POETRY_CACHE_DIR

RUN chmod +x /app/docker-entrypoint.sh

ENTRYPOINT [ "/app/docker-entrypoint.sh" ]