# Configurando o Atalho no iPhone (passo a passo detalhado)

Esse guia monta o Atalho "Meu Agente" que:

1. Você chama pela Siri dizendo "Ei Siri, meu agente"
2. Ele ativa o ditado — você fala o que quer (ex: "cria um lembrete pra tomar remédio amanhã às 9")
3. Envia o texto pro backend em `backend/` (rota `POST /voice`)
4. Se o backend interpretar como pedido de lembrete, cria o lembrete no app nativo
5. A Siri fala em voz alta a confirmação

**Como funciona a invocação pela Siri**: a Siri usa o *nome do Atalho* como frase de ativação automaticamente. Salvando o Atalho com o nome "Meu Agente", "Ei Siri, meu agente" já dispara ele — não precisa configurar mais nada.

## Antes de começar

Tenha em mãos:
- A URL do backend (ex: `https://ia-engineering-journey.onrender.com`)
- O valor de `AGENT_API_KEY` configurado no Render

## Criando o Atalho

1. Abra o app **Atalhos** (ícone azul e roxo, já vem instalado no iPhone)
2. Na barra inferior, toque em **Atalhos**
3. Toque no **+** no canto superior direito
4. Toque no nome no topo (aparece como "Novo Atalho") e renomeie para **Meu Agente**

### Ação 1 — Ditar Texto

5. Na caixa de busca "Buscar apps e ações", digite `ditar`
6. Toque em **Ditar Texto**
7. Dentro da ação, toque em **Mostrar Mais** e mude o idioma para **Português (Brasil)**

### Ação 2 — Obter Conteúdo de URL

8. Busque `obter conteúdo` e toque em **Obter Conteúdo de URL**
9. No campo **URL**, cole a URL do backend + `/voice`, ex:
   `https://ia-engineering-journey.onrender.com/voice`
10. Toque em **Mostrar Mais** para expandir as opções
11. **Método**: mude de GET para **POST**
12. **Cabeçalhos**: toque em "Adicionar novo cabeçalho" duas vezes e preencha:
    - Chave `Content-Type` → Valor `application/json`
    - Chave `X-Api-Key` → Valor (o mesmo `AGENT_API_KEY` do Render)
13. **Corpo da requisição**: mude para **JSON**
14. Toque em "Adicionar novo campo" → escolha tipo **Texto**
    - Chave: `text`
    - Valor: toque no campo — nas sugestões azuis acima do teclado, escolha a variável **Texto Ditado** (vem da ação 1)

### Ação 3 — Obter Valor do Dicionário (para o campo `action`)

15. Busque `obter valor do dicionário`
16. Chave: `action`
17. Dicionário: variável **Conteúdo de URL** (aparece automaticamente)

### Ação 4 — Se

18. Busque `Se` e escolha a ação **Se**
19. Configure a condição:
    - Entrada: variável **Valor do Dicionário** (do passo 15)
    - Operador: **é**
    - Valor: digite `create_reminder`

Aparecerão dois blocos: **Então** e **Caso Contrário**.

### Dentro do bloco "Então"

20. Adicione **Obter Valor do Dicionário** com Chave = `title`, Dicionário = "Conteúdo de URL". Renomeie o resultado para `titulo` (para não confundir com os outros).
21. Adicione outro **Obter Valor do Dicionário** com Chave = `due_date`. Renomeie para `data_iso`.
22. Adicione outro **Obter Valor do Dicionário** com Chave = `notes`. Renomeie para `notas`.
23. Adicione **Obter Datas a partir da Entrada** com Entrada = variável `data_iso`.
24. Adicione **Adicionar Novo Lembrete**:
    - Título = variável `titulo`
    - Toque em **Mostrar Mais**
    - Lembrete em: **Lembretes** (a lista padrão, ou escolha outra)
    - Vencimento: variável **Data** (o resultado do passo 23)
    - Notas: variável `notas`

### Depois do bloco "Fim Se" — falar a confirmação

25. Adicione **Obter Valor do Dicionário** com Chave = `reply`, Dicionário = "Conteúdo de URL". Renomeie para `resposta`.
26. Adicione **Falar Texto** com o texto = variável `resposta`. Em Mostrar Mais, escolha idioma **Português (Brasil)**.

### Salvar

27. Toque em **Concluído** (ou **OK**) no canto superior direito.

## Testando

Com o iPhone desbloqueado (ou pela CarPlay/AirPods, se estiver configurado):

> "Ei Siri, meu agente"

A Siri abre o atalho e ativa o ditado — fale em seguida:

> "cria um lembrete pra pagar o boleto amanhã às 18h"

Se der tudo certo, o app Lembretes vai ter o item novo e a Siri vai falar em voz alta a confirmação.

Na primeira execução, o iOS pede permissão para o atalho acessar Lembretes — aceite.

## Solução de problemas

- **"Não consegui contatar o servidor"**: teste a rota `/health` do backend no Safari. Se demorar muito, é o serviço acordando (o plano free do Render "dorme" quando fica ocioso, e leva ~30-50s pra subir).
- **Erro 401**: o valor de `X-Api-Key` no atalho não está exatamente igual ao `AGENT_API_KEY` do Render.
- **Lembrete criado sem a data**: o parser de datas dos Atalhos pode não reconhecer a string ISO. Teste tirar o passo "Obter Datas a partir da Entrada" e colocar a variável `data_iso` direto no campo Vencimento.
- **A Siri não abre o atalho ao dizer o nome**: confirme que o atalho foi salvo com o nome exato "Meu Agente" e que a Siri está ativada em Ajustes → Siri e Busca.
