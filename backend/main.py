from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import asyncpg
import time
import datetime
from prometheus_fastapi_instrumentator import Instrumentator

# Connexion PostgreSQL
DB_URL = os.getenv("DATABASE_URL", "postgresql://user:password@postgres:5432/mydb")

# Configuration de l'instrumentation Prometheus
instrumentator = Instrumentator()
    
# Fonction pour vérifier la connexion à la base de données
@asynccontextmanager
async def lifespan(app: FastAPI):
    instrumentator.expose(app)
    app.state.db = await asyncpg.create_pool(DB_URL)
    app.state.start_time = time.time()
    try:
        yield
    finally:
        await app.state.db.close()

app = FastAPI(lifespan=lifespan)
instrumentator.instrument(app)

# Configuration des règles CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Autoriser toutes les origines (à restreindre en prod)
    allow_credentials=True,
    allow_methods=["*"],  # Autoriser toutes les méthodes (GET, POST, etc.)
    allow_headers=["*"],  # Autoriser tous les headers
)

@app.get("/compute")
def compute():
    def fibonacci(n):
        if n <= 1:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)

    start = time.time()
    result = fibonacci(30)
    duration = time.time() - start
    return {"result": result, "duration": duration} #time in seconds

@app.get("/io")
async def io():
    start = time.time()
    async with app.state.db.acquire() as connection:
        rows = await connection.fetch("SELECT * FROM users LIMIT 5")
    duration = time.time() - start
    return {
        "users": [dict(row) for row in rows],
        "duration": duration
    }

@app.get("/status")
def status():
    uptime = time.time() - app.state.start_time
    return {
        "status": "ok",
        "uptime_seconds": round(uptime, 2),
        "time": datetime.datetime.now().isoformat()
    }

@app.get("/crash")
def crash():
    os._exit(1)
# ---------------------------------------------------------------------------------------------------------|#
# @app.get("/health")
# def health():
#     try:
#         with app.state.db.acquire() as connection:
#             connection.execute("SELECT 1")
#         return {"status": "ok"}
#     except Exception as e:
#         return {"status": "error", "error": str(e)}
    
# @app.get("/metrics")
# def metrics():
#     return {
#         "uptime": datetime.datetime.now() - app.state.start_time,
#         "requests": app.state.request_count,
#         "errors": app.state.error_count
#     }

# @app.get("/slow")
# def slow():
#     time.sleep(5)
#     return {"status": "ok"}

# @app.get("/error")
# def error():
#     raise Exception("This is a test error")

# @app.get("/timeout")
# def timeout():
#     time.sleep(10)
#     return {"status": "ok"}

# @app.get("/db")
# def db():
#     try:
#         with app.state.db.acquire() as connection:
#             connection.execute("SELECT 1")
#         return {"status": "ok"}
#     except Exception as e:
#         return {"status": "error", "error": str(e)}

# # ---------------------------------------------------------------------------------------------------------|#
# @app.get("/db/slow")
# def db_slow():
#     time.sleep(5)
#     try:
#         with app.state.db.acquire() as connection:
#             connection.execute("SELECT 1")
#         return {"status": "ok"}
#     except Exception as e:
#         return {"status": "error", "error": str(e)}

# @app.get("/db/error")
# def db_error():
#     try:
#         with app.state.db.acquire() as connection:
#             connection.execute("SELECT * FROM non_existent_table")
#         return {"status": "ok"}
#     except Exception as e:
#         return {"status": "error", "error": str(e)}
    
# @app.get("/db/timeout")
# def db_timeout():
#     time.sleep(10)
#     try:
#         with app.state.db.acquire() as connection:
#             connection.execute("SELECT 1")
#         return {"status": "ok"}
#     except Exception as e:
#         return {"status": "error", "error": str(e)}

# @app.get("/db/health")
# def db_health():
#     try:
#         with app.state.db.acquire() as connection:
#             connection.execute("SELECT 1")
#         return {"status": "ok"}
#     except Exception as e:
#         return {"status": "error", "error": str(e)}
    
# @app.get("/db/metrics")
# def db_metrics():
#     try:
#         with app.state.db.acquire() as connection:
#             connection.execute("SELECT 1")
#         return {
#             "status": "ok",
#             "uptime_seconds": round(time.time() - app.state.start_time, 2),
#             "time": datetime.datetime.now().isoformat()
#         }
#     except Exception as e:
#         return {"status": "error", "error": str(e)}

# @app.get("/db/status")
# def db_status():
#     try:
#         with app.state.db.acquire() as connection:
#             connection.execute("SELECT 1")
#         return {
#             "status": "ok",
#             "uptime_seconds": round(time.time() - app.state.start_time, 2),
#             "time": datetime.datetime.now().isoformat()
#         }
#     except Exception as e:
#         return {"status": "error", "error": str(e)}


# @app.get("/db/crash")
# def db_crash():
#     try:
#         with app.state.db.acquire() as connection:
#             connection.execute("SELECT 1")
#         os._exit(1)
#     except Exception as e:
#         return {"status": "error", "error": str(e)}
    

# Pour lancer : uvicorn main:app --reload --host 0.0.0.0 --port 8000
