# syntax=docker/dockerfile:1

## build our base image (used for all stages except prod)
FROM python:3.12-slim AS base

# set our env vars
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    LANG=C.UTF-8

RUN --mount=type=bind,source=requirements.lock,target=requirements.lock \
    pip install --no-cache-dir -r requirements.lock

FROM base AS final

RUN groupadd -g 999 python && \
    useradd -r -u 999 -g python -m python

EXPOSE 8000

USER 999

WORKDIR /app/src

COPY --chown=999:999 ./src/ .


FROM final AS develop

RUN --mount=type=bind,source=requirements-dev.lock,target=requirements-dev.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    pip install --no-cache-dir -r requirements-dev.lock

ENTRYPOINT ["uvicorn", "--host", "0.0.0.0", "--reload", "triangler.app:app"]


FROM final AS prod

ENTRYPOINT ["uvicorn", "--host", "0.0.0.0", "triangler.app:app"]
