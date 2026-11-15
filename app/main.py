import os
import sqlite3
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, Field

DB_PATH = os.getenv("DATABASE_PATH", "data/tarefas.db")


def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@asynccontextmanager
async def lifespan(app: FastAPI):
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    with connect() as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS tarefas (id INTEGER PRIMARY KEY AUTOINCREMENT, titulo TEXT NOT NULL, descricao TEXT NOT NULL, concluida INTEGER NOT NULL DEFAULT 0)")
    yield


app = FastAPI(title="Lista de Tarefas", version="1.0.0", lifespan=lifespan,
              description="API REST para criar, consultar, atualizar e excluir tarefas.")


class TarefaEntrada(BaseModel):
    titulo: str = Field(min_length=1, max_length=200, pattern=r"\S")
    descricao: str = Field(default="", max_length=2000)
    concluida: bool = False


class TarefaSaida(TarefaEntrada):
    id: int


@app.get("/", tags=["Saúde"])
def inicio():
    return {"aplicacao": "Lista de Tarefas", "docs": "/docs"}


@app.get("/health", tags=["Saúde"])
def health():
    return {"status": "ok", "version": os.getenv("APP_VERSION", "local")}


@app.post("/tarefas", response_model=TarefaSaida, status_code=201, tags=["Tarefas"])
def criar(tarefa: TarefaEntrada):
    with connect() as conn:
        cur = conn.execute("INSERT INTO tarefas (titulo, descricao, concluida) VALUES (?, ?, ?)",
                           (tarefa.titulo, tarefa.descricao, tarefa.concluida))
        return {"id": cur.lastrowid, **tarefa.model_dump()}


@app.get("/tarefas", response_model=list[TarefaSaida], tags=["Tarefas"])
def listar():
    with connect() as conn:
        return [dict(row) for row in conn.execute("SELECT * FROM tarefas ORDER BY id")]


@app.get("/tarefas/{tarefa_id}", response_model=TarefaSaida, tags=["Tarefas"])
def consultar(tarefa_id: int):
    with connect() as conn:
        row = conn.execute("SELECT * FROM tarefas WHERE id = ?", (tarefa_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return dict(row)


@app.put("/tarefas/{tarefa_id}", response_model=TarefaSaida, tags=["Tarefas"])
def atualizar(tarefa_id: int, tarefa: TarefaEntrada):
    with connect() as conn:
        cur = conn.execute("UPDATE tarefas SET titulo = ?, descricao = ?, concluida = ? WHERE id = ?",
                           (tarefa.titulo, tarefa.descricao, tarefa.concluida, tarefa_id))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return {"id": tarefa_id, **tarefa.model_dump()}


@app.delete("/tarefas/{tarefa_id}", status_code=204, tags=["Tarefas"])
def remover(tarefa_id: int):
    with connect() as conn:
        cur = conn.execute("DELETE FROM tarefas WHERE id = ?", (tarefa_id,))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return Response(status_code=204)
