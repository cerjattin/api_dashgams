from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pyodbc

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=datagams.mssql.somee.com;"
        "DATABASE=datagams;"
        "UID=DevGams_SQLLogin_1;"
        "PWD=uffsfthge8;"
        "TrustServerCertificate=yes;"
    )

@app.get("/")
def root():
    return {"status": "OK", "message": "API Dashboard funcionando"}

@app.get("/ventas")
def get_ventas():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            SELECT 
                id,
                ano,
                periodo,
                mes,
                cod_ven,
                vendedor,
                ventas,
                meta1,
                meta2,
                cumplimiento1,
                cumplimiento2,
                fecha_actualizacion
            FROM VENTAS_RESUMEN
            ORDER BY ano, periodo
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        data = []
        for r in rows:
            data.append({
                "id": r.id,
                "año": r.ano,
                "periodo": r.periodo,
                "mes": r.mes,
                "cod_ven": r.cod_ven,
                "vendedor": r.vendedor,
                "ventas": float(r.ventas or 0),
                "meta1": float(r.meta1 or 0),
                "meta2": float(r.meta2 or 0),
                "cumplimiento1": float(r.cumplimiento1 or 0),
                "cumplimiento2": float(r.cumplimiento2 or 0),
                "fecha_actualizacion": str(r.fecha_actualizacion)
            })

        return {
            "success": True,
            "count": len(data),
            "data": data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
