FROM ubuntu:22.04
ARG DISTRO
ARG VERSION

RUN apt-get update && apt-get install -y \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/*
