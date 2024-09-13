from fastapi import FastAPI
from main import router
from database import init_db

app = FastAPI()

@app.on_event("startup")
def startup_event():
    init_db()  # Inicializa o banco de dados

# Inclui o roteador definido em main.py
app.include_router(router, prefix='/api/geek')