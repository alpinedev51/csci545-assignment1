FROM python:3.13-slim-bookworm

ARG APP_VERSION
ENV APP_VERSION=$APP_VERSION

LABEL maintainer="Austin Barton <atb51@protonmail.com>"

RUN apt -y update && apt -y upgrade && \
	apt -y install procps libpq-dev gcc

WORKDIR /scs/
COPY . .

RUN python -m pip install --upgrade pip
RUN pip install uv
RUN uv venv
RUN uv sync --no-dev --frozen

RUN chmod +x ./run_server.sh
CMD ["./run_server.sh"]
