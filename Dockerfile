# Imagen base Debian 12 + Python 3.11 (compatibles con Microsoft)
FROM python:3.11-slim-bookworm

# Evitar prompts interactivos
ENV DEBIAN_FRONTEND=noninteractive

# Instalar utilidades y dependencias
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gnupg \
    apt-transport-https \
    ca-certificates \
    unixodbc-dev && \
    rm -rf /var/lib/apt/lists/*

# Agregar repositorio Microsoft (Bookworm)
RUN curl -sSL https://packages.microsoft.com/config/debian/12/prod.list \
    -o /etc/apt/sources.list.d/mssql-release.list

# Agregar keyring oficial
RUN curl -sSL https://packages.microsoft.com/keys/microsoft.asc \
    | gpg --dearmor \
    | tee /usr/share/keyrings/microsoft-prod.gpg > /dev/null

# Instalar msodbcsql18
RUN apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql18 && \