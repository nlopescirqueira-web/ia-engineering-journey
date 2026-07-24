# Voice Agent — backend

API que recebe texto (transcrito por um Atalho do iPhone), usa a Claude API para
entender a intenção e, por enquanto, sabe executar uma única função:
**criar lembrete**. Cada interação é registrada em um banco SQLite.

## Rodando localmente

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # preencha ANTHROPIC_API_KEY e AGENT_API_KEY
export $(cat .env | xargs)
uvicorn main:app --reload
```

Teste:

```bash
curl -X POST http://localhost:8000/voice \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: $AGENT_API_KEY" \
  -d '{"text": "me lembra de comprar leite amanhã às 18h"}'
```

## Rota

`POST /voice`

- **Entrada**: `{"text": "..."}`
- **Saída**: `{"action": "create_reminder" | "none", "title", "due_date", "notes", "reply"}`
- **Auth**: header `X-Api-Key` (deve bater com `AGENT_API_KEY`, se essa variável estiver definida).

## Deploy no Render

1. Crie um **Web Service** apontando para este repositório.
2. **Root Directory**: `backend`
3. **Build Command**: `pip install -r requirements.txt`
4. **Start Command**: `python3 -m uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Defina as variáveis de ambiente `ANTHROPIC_API_KEY` e `AGENT_API_KEY` no dashboard.

Há também um `render.yaml` na raiz do repo como blueprint inicial — confira os campos no dashboard do Render, já que o formato do blueprint pode mudar.

## Limitação atual

O banco é SQLite em arquivo local (`backend/data/agent.db`). No plano gratuito do
Render o disco não é persistente entre deploys — os dados podem ser perdidos a
cada novo deploy. Para persistência de verdade, trocar por Postgres (o Render
tem um plano free de Postgres) é o próximo passo natural.
