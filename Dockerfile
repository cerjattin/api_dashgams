# Imagen base con Python 3.11
FROM python:3.11-slim

# Instalar dependencias necesarias para pyodbc y herramientas del sistema
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        gnupg \
        apt-transport-https \
        unixodbc-dev \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Agregar repositorio de Microsoft de forma correcta (sin apt-key)
RUN curl -sSL https://packages.microsoft.com/config/debian/12/prod.list \
    -o /etc/apt/sources.list.d/mssql-release.list

# Importar clave de Microsoft usando /usr/share/keyrings (método moderno)
RUN curl -sSL https://packages.microsoft.com/keys/microsoft.asc \
    | gpg --dearmor \
    | tee /usr/share/keyrings/microsoft.gpg > /dev/null

# Instalar driver msodbcsql18
RUN apt-get update \
    && ACCEPT_EULA=Y apt-get install -y --no-install-recommends \
        msodbcsql18 \
    && rm -rf /var/lib/apt/lists/*

# Crear carpeta de trabajo
WORKDIR /app

# Copiar dependencias
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar la aplicación
COPY . .

# Exponer API
EXPOSE 8000

# Comando principal
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
