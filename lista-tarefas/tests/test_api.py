import pytest
from fastapi.testclient import TestClient
from app import main


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(main, "DB_PATH", str(tmp_path / "test.db"))
    with TestClient(main.app) as c:
        yield c


def test_crud(client):
    assert client.get("/tarefas").json() == []
    r = client.post("/tarefas", json={"titulo": "Entregar atividade", "descricao": "CI/CD"})
    assert r.status_code == 201
    tid = r.json()["id"]
    assert len(client.get("/tarefas").json()) == 1
    assert client.get(f"/tarefas/{tid}").json()["titulo"] == "Entregar atividade"
    r = client.put(f"/tarefas/{tid}", json={"titulo": "Entregar atividade", "concluida": True})
    assert r.status_code == 200 and r.json()["concluida"] is True
    assert client.delete(f"/tarefas/{tid}").status_code == 204
    assert client.get(f"/tarefas/{tid}").status_code == 404
    assert client.get("/tarefas").json() == []


@pytest.mark.parametrize("titulo", ["", "   ", "x" * 201])
def test_titulo_invalido(client, titulo):
    assert client.post("/tarefas", json={"titulo": titulo}).status_code == 422


def test_nao_encontrada(client):
    assert client.put("/tarefas/999", json={"titulo": "Teste"}).status_code == 404
    assert client.delete("/tarefas/999").status_code == 404


def test_docs_e_saude(client):
    assert client.get("/docs").status_code == 200
    assert client.get("/health").json()["status"] == "ok"
    assert "/tarefas" in client.get("/openapi.json").json()["paths"]

