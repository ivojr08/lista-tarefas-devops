# Lista de Tarefas — FastAPI e CI/CD

API REST acadêmica para cadastrar, listar, consultar, atualizar e remover tarefas.

## Tecnologias
Python 3.11, FastAPI, Pydantic, SQLite, Uvicorn, pytest, HTTPX, Docker,
GitHub Actions, GitHub Container Registry (GHCR) e Render.

## Execução local
No terminal, dentro da pasta do projeto:

```bash
python -m venv .venv
```

Windows PowerShell:
```powershell
.venv\Scripts\Activate.ps1
```
Linux/macOS:
```bash
source .venv/bin/activate
```

```bash
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

Acesse http://127.0.0.1:8000/docs. Testes: `python -m pytest -v`.

## Docker
```bash
docker build -t lista-tarefas .
docker run --rm -p 8000:8000 lista-tarefas
```

## Rotas
| Método | Rota | Finalidade |
|---|---|---|
| GET | /health | Saúde e versão (SHA do commit na imagem) |
| GET | /docs | Documentação interativa |
| POST | /tarefas | Criar tarefa, HTTP 201 |
| GET | /tarefas | Listar tarefas |
| GET | /tarefas/{id} | Consultar tarefa |
| PUT | /tarefas/{id} | Substituir dados da tarefa |
| DELETE | /tarefas/{id} | Excluir tarefa, HTTP 204 |

Exemplo de corpo para POST ou PUT:
```json
{"titulo":"Entregar atividade DevOps","descricao":"Validar pipeline CI/CD","concluida":false}
```

## Integração e entrega contínuas
O workflow `.github/workflows/ci-cd.yml` executa testes e valida a construção
Docker em pull requests destinados à main e em pushes para main.
Após sucesso na main, publica no GHCR as tags `latest` e o SHA completo do commit.
O login usa o GITHUB_TOKEN automático com permissão packages:write.
Após configurar o Render, o terceiro job solicita a implantação da tag do commit
pelo deploy hook e consulta /health até confirmar esse SHA em execução.
PRs executam somente CI. Nunca recebem credenciais de implantação.

## Configuração do Render e do GitHub
Veja PASSO_A_PASSO.md. São necessários:
- Secret `RENDER_DEPLOY_HOOK_URL` no GitHub.
- Variable `RENDER_SERVICE_URL` com a URL pública do serviço, sem /docs.

O job de implantação é ignorado enquanto a variável não existir, permitindo
publicar a primeira imagem antes de criar o serviço Render. Essa execução inicial
não comprova a implantação automatizada; execute novamente após a configuração.

## Armazenamento e limitações
SQLite armazena os dados em data/tarefas.db (configurável por DATABASE_PATH).
No Render sem disco persistente, os dados podem ser perdidos em reinicializações
ou implantações. Esta demonstração acadêmica não tem autenticação e não deve
receber dados pessoais. Para uso real, adotar autenticação e banco persistente.

## Referências
- https://fastapi.tiangolo.com/
- https://docs.github.com/en/actions/tutorials/publish-packages/publish-docker-images
- https://render.com/docs/deploy-hooks
