# Imagen base compatible con Microsoft ODBC (Debian 12)
FROM python:3.11-slim-bookworm

ENV DEBIAN_FRONTEND=noninteractive

# Dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gnupg \
    apt-transport-https \
    ca-certificates \
    unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*

# Repositorio Microsoft para Debian 12
RUN curl -sSL https://packages.microsoft.com/config/debian/12/prod.list \
    -o /etc/apt/sources.list.d/mssql-release.list

# Keyring Microsoft
RUN curl -sSL https://packages.microsoft.com/keys/microsoft.asc \
    | gpg --dearmor \
    | tee /usr/share/keyrings/microsoft-prod.gpg > /dev/null

# Instalar msodbcsql18
RUN apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql18 && \
    rm -rf /var/lib/apt/lists/*

# Crear carpeta app
WORKDIR /app

# Copiar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Exponer API
EXPOSE 8000

# Iniciar servidor
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
