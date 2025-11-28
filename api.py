# api.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pyodbc
from typing import Optional
from datetime import datetime

app = FastAPI(title="Dashboard Ventas - API Oficial")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Datos de conexión
DB_CONFIG = {
    'server': 'datagams.mssql.somee.com',
    'database': 'datagams',
    'username': 'DevGams_SQLLogin_1',
    'password': 'uffsfthge8',
    'driver': '{ODBC Driver 17 for SQL Server}'
}

def get_connection():
    try:
        conn_str = (
            f"DRIVER={DB_CONFIG['driver']};"
            f"SERVER={DB_CONFIG['server']};"
            f"DATABASE={DB_CONFIG['database']};"
            f"UID={DB_CONFIG['username']};"
            f"PWD={DB_CONFIG['password']};"
            "Encrypt=yes;"
            "TrustServerCertificate=yes;"
        )
        return pyodbc.connect(conn_str, timeout=30)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión SQL: {str(e)}")


# ------------------------------------------------------
# ENDPOINTS
# ------------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "API Dashboard Ventas ONLINE",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
def health():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM VENTAS_RESUMEN")
        count = cursor.fetchone()[0]
        return {
            "status": "healthy",
            "registros": count,
            "timestamp": datetime.now()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }


# ------------------------------------------------------
# OBTENER VENTAS
# ------------------------------------------------------

@app.get("/ventas")
def get_ventas(año: Optional[int] = None, vendedor: Optional[str] = None):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        SELECT ano, periodo, mes, vendedor, ventas, meta1, cumplimiento1
        FROM VENTAS_RESUMEN
        WHERE 1 = 1
        """

        params = []

        if año:
            query += " AND ano = ?"
            params.append(año)

        if vendedor:
            query += " AND vendedor = ?"
            params.append(vendedor)

        query += " ORDER BY ano DESC, periodo ASC"

        cursor.execute(query, params)
        rows = cursor.fetchall()

        data = []
        for r in rows:
            data.append({
                "año": r[0],
                "periodo": r[1],
                "mes": r[2],
                "vendedor": r[3],
                "ventas": float(r[4]),
                "meta": float(r[5]),
                "cumplimiento": float(r[6])
            })

        return {
            "success": True,
            "count": len(data),
            "data": data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/vendedores")
def get_vendedores():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT DISTINCT vendedor FROM VENTAS_RESUMEN ORDER BY vendedor")
        vendedores = [row[0] for row in cursor.fetchall()]

        return {
            "success": True,
            "vendedores": vendedores
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/años")
def get_años():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT DISTINCT ano FROM VENTAS_RESUMEN ORDER BY ano DESC")
        años = [row[0] for row in cursor.fetchall()]

        return {
            "success": True,
            "años": años
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ------------------------------------------------------
# RESUMEN GENERAL
# ------------------------------------------------------

@app.get("/ventas/resumen")
def resumen():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        SELECT
            COUNT(*),
            SUM(ventas),
            AVG(ventas)
        FROM VENTAS_RESUMEN
        """

        cursor.execute(query)
        total, suma, promedio = cursor.fetchone()

        return {
            "success": True,
            "resumen": {
                "total_registros": total,
                "total_ventas": float(suma),
                "promedio_ventas": float(promedio)
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Ejecutar
if __name__ == "__main__":
    import uvicorn
    print("🚀 API ONLINE en http://localhost:8000  — Dashboard listo para conectar")
    uvicorn.run(app, host="0.0.0.0", port=8000)
