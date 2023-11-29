ARG PYTHON_VERSION=3.10.4
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout
ENV PYTHONUNBUFFERED=1

WORKDIR .
COPY . .

# Deps setup
RUN pip install --upgrade pip
RUN rm -rf poetry.lock && pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install && rm -rf msrv.egg-info build


# Installling dev deps just in case
RUN pip install -r  scripts/requires.dev.txt

# over at the host only
CMD uvicorn msrv.run:apx --host=0.0.0.0 --port=8000
