# Publicar e reunir as evidências

## 1. Criar o repositório
1. Entre no GitHub e crie um repositório chamado lista-tarefas-devops.
2. Use main como branch principal. Pode ser público; se privado, convide
   hrchlhck em Settings > Collaborators.
3. Extraia o ZIP. Envie o conteúdo de lista-tarefas para a raiz do repositório.
   Não envie o ZIP como um único arquivo. Inclua a pasta .github!
4. Pelo navegador, se a pasta .github não for enviada, use Add file > Create new
   file e informe .github/workflows/ci-cd.yml; copie o conteúdo do arquivo local.
   A raiz precisa conter Dockerfile, requirements.txt, app/, tests/ e .github/.
5. Abra Actions. Aguarde CI e CD verdes. O deploy inicialmente será ignorado.

Alternativa com Git instalado, na pasta extraída (substitua SEU_USUARIO):
```bash
git init -b main
git add .
git commit -m "Implementa API de tarefas e pipeline CI/CD"
git remote add origin https://github.com/SEU_USUARIO/lista-tarefas-devops.git
git push -u origin main
```

## 2. Disponibilizar a imagem
1. No seu perfil GitHub, abra Packages e o pacote lista-tarefas-devops.
2. Em Package settings, torne o pacote público para o Render baixar sem senha.
   A visibilidade do pacote pode ser privada mesmo com repositório público.
3. Copie o nome da imagem: ghcr.io/seu_usuario/lista-tarefas-devops:latest.
   O nome é em letras minúsculas. Capture a página com as tags publicadas.

## 3. Implantar no Render
1. No Render, New > Web Service > Existing Image (imagem existente).
2. Informe a imagem do passo anterior. Não escolha implantação pelo código Git.
3. Escolha a instância gratuita se disponível. Não confirme plano pago sem querer.
4. Use /health como Health Check Path. O comando vem do Dockerfile.
5. Aguarde o serviço ficar Live. Copie a URL pública.
6. Abra URL/docs e confira os endpoints. Abra URL/health.
7. Em Settings, localize Deploy Hook e copie o endereço secreto.

## 4. Conectar CD ao Render
No repositório GitHub: Settings > Secrets and variables > Actions.
1. Na aba Secrets, New repository secret:
   nome RENDER_DEPLOY_HOOK_URL; valor é o Deploy Hook do Render.
2. Na aba Variables, New repository variable:
   nome RENDER_SERVICE_URL; valor https://SEU-SERVICO.onrender.com.
3. Não inclua a URL secreta nos prints ou no relatório.

## 5. Executar um pull request real
1. No GitHub, edite o README (por exemplo, acrescente seu nome).
2. Ao salvar, escolha criar uma nova branch, como evidencia-ci.
3. Abra o pull request dessa branch para main.
4. Aguarde CI passar. Tire prints do PR e da execução com testes/build verdes.
5. Faça Merge pull request. O push em main acionará CI, publicação e implantação.
6. Aguarde todos os jobs verdes, incluindo Implantar e verificar Render.
7. Capture o log Confirmar versao em execucao: ele mostra o SHA confirmado.
8. Capture o pacote GHCR com a tag SHA e o Render com o deploy Live.

## 6. Testar e capturar a API implantada
Na URL/docs, capture primeiro a visão geral com o endereço visível.
1. Abra POST /tarefas > Try it out. Use:
   {"titulo":"Entregar atividade DevOps","descricao":"Evidência REST","concluida":false}
   Clique Execute e capture corpo e resposta 201. Anote o id retornado.
2. Abra GET /tarefas > Try it out > Execute. Capture resposta 200 e a tarefa.
3. Abra PUT /tarefas/{tarefa_id}, informe o id, use o mesmo título e concluida=true.
   Execute e capture resposta 200 com concluida=true.
4. Opcional: DELETE com o id; capture resposta 204.
5. Abra /health: o valor version deve corresponder à tag SHA da última imagem.

## 7. Relatório técnico final
Envie os links do repositório, pacote e aplicação, além dos prints dos passos
anteriores, para montar o PDF. Identifique as imagens:
01-docs; 02-criacao; 03-listagem; 04-atualizacao; 05-ci-pr;
06-ci-etapas; 07-cd; 08-imagem; 09-render-live; 10-health-versao.
O relatório deve conter identificação, objetivo, implementação REST, CI,
CD (com trecho real do workflow), implantação, resultados e link do repositório.
Não declare execução ou implantação concluída antes das evidências reais.
