# ia-engineering-journey
Esse vai ser meu diário público de estudos pelos próximos meses
Dia 1 - ambiente configurado

## Projeto: agente de voz via Atalhos do iPhone

Teste de um agente que recebe voz (ditada por um Atalho do iPhone), usa a
Claude API para interpretar o pedido e, por enquanto, sabe executar uma única
ação: criar lembretes. Cada interação fica registrada em um banco SQLite.

- Backend: [`backend/`](backend/) (FastAPI + Claude API + SQLite)
- Como montar o Atalho no iPhone: [`docs/shortcuts-setup.md`](docs/shortcuts-setup.md)