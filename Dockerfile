# https://github.com/GoogleContainerTools/distroless/blob/master/examples/python3-requirements/Dockerfile

FROM debian:10-slim AS build
# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get install --no-install-suggests --no-install-recommends --yes \
        python3-venv \
        gcc \
        libpython3-dev && \
    python3 -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

FROM build AS build-venv
COPY requirements.txt /requirements.txt
RUN /venv/bin/pip install --disable-pip-version-check -r /requirements.txt

FROM gcr.io/distroless/python3-debian10:nonroot-amd64
COPY --from=build-venv /venv /venv
COPY feed /wyin-be-feed/feed
WORKDIR /wyin-be-feed
EXPOSE 8080
ARG BUILD_VERSION="latest"
ENV API_VERSION=$BUILD_VERSION
ENTRYPOINT ["/venv/bin/uvicorn", "feed.main:app", "--host", "0.0.0.0", "--port", "8080"]
