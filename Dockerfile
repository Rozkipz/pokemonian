FROM python:3.9

ENV POETRY_VERSION=1.1.8
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /code
COPY . /code/

RUN poetry install  #  --no-dev  # commented out so i can use the same container for the tests.

ENTRYPOINT ["/bin/sh", "-c"]
