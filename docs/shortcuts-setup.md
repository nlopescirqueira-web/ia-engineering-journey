# Configurando o Atalho no iPhone

Este guia monta o Atalho que fala com o backend em `backend/` (rota `POST /voice`).

Fluxo do Atalho: **Ditado → chama o backend → cria o lembrete nativo → fala a confirmação.**

## Passo a passo

1. Abra o app **Atalhos** → toque em **+** para criar um novo atalho.
2. Adicione a ação **Ditar Texto** (Dictate Text). Deixe o idioma em Português.
3. Adicione a ação **Obter Conteúdo de URL** (Get Contents of URL):
   - **URL**: `https://SEU-APP.onrender.com/voice`
   - **Método**: `POST`
   - **Cabeçalhos**:
     - `Content-Type`: `application/json`
     - `X-Api-Key`: `<mesmo valor de AGENT_API_KEY no backend>`
   - **Corpo da requisição**: JSON, com o campo `text` = variável **Texto Ditado**.
4. Adicione **Obter Valor do Dicionário** (Get Dictionary Value) para pegar cada campo do JSON retornado: `action`, `title`, `due_date`, `notes`, `reply`. (Ou use diretamente `Conteúdo de URL.action`, etc., como variáveis mágicas.)
5. Adicione um bloco **Se** (If): `action` é igual a `create_reminder`.
   - **Então**:
     - Adicione **Obter Datas a partir da Entrada** (Get Dates from Input) sobre o valor de `due_date`, para converter a string ISO em um objeto Data.
     - Adicione **Adicionar Novo Lembrete** (Add New Reminder):
       - Título = `title`
       - Notas = `notes`
       - Data de vencimento = data obtida no passo anterior
   - **Senão**: nada a fazer (o lembrete não foi criado).
6. Fora do bloco Se, adicione **Falar Texto** (Speak Text) = `reply`, para o Atalho confirmar em voz alta o que entendeu (funciona tanto para o caso de sucesso quanto para o caso em que o pedido não era sobre lembrete).
7. Nomeie o Atalho (ex: "Assistente") e, se quiser, ative **Adicionar à Siri** com uma frase de ativação para rodar totalmente por voz, mãos livres.

## Observações

- A conversão de `due_date` (string ISO) para Data pode precisar de ajuste fino — o parser de datas dos Atalhos às vezes é sensível ao formato. Teste com frases como "me lembra de pagar o boleto amanhã às 9h" e ajuste a ação de conversão se necessário.
- Guarde o valor de `AGENT_API_KEY` em local seguro; ele é o que impede qualquer pessoa de usar seu endpoint público no Render.
- Para depurar, chame a rota `GET /health` do backend pelo navegador para confirmar que o deploy está no ar.
