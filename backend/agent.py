import os
from datetime import datetime
from zoneinfo import ZoneInfo

import anthropic

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

MODEL = "claude-sonnet-5"

TOOLS = [
    {
        "name": "create_reminder",
        "description": (
            "Cria um lembrete para o usuário. Use somente quando o usuário pedir "
            "explicitamente para lembrar de algo, marcar um compromisso ou criar "
            "um lembrete."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Título curto e claro do lembrete.",
                },
                "due_date": {
                    "type": "string",
                    "description": (
                        "Data/hora do lembrete em ISO 8601 (YYYY-MM-DDTHH:MM:SS), "
                        "resolvida a partir de termos relativos como 'amanhã' ou "
                        "'às 18h' usando a data/hora atual informada no system "
                        "prompt. Omita se nenhum horário específico foi mencionado."
                    ),
                },
                "notes": {
                    "type": "string",
                    "description": "Notas ou detalhes adicionais do lembrete, se houver.",
                },
            },
            "required": ["title"],
        },
    }
]


def _system_prompt() -> str:
    now = datetime.now(ZoneInfo("America/Sao_Paulo"))
    return (
        "Você é um assistente de voz pessoal. Hoje é "
        f"{now.strftime('%A, %d/%m/%Y')}, agora são {now.strftime('%H:%M')} "
        "(horário de Brasília).\n\n"
        "Por enquanto você só sabe executar UMA ação: criar lembretes, através "
        "da tool create_reminder. Se o pedido do usuário não for sobre criar um "
        "lembrete, NÃO chame nenhuma tool - apenas responda em poucas palavras, "
        "em português, explicando que ainda não sabe fazer isso.\n\n"
        "Quando chamar create_reminder, escreva antes uma frase curta em "
        "português confirmando o que foi entendido, para ser falada em voz alta "
        "pelo Atalho."
    )


def process_voice_command(text: str) -> dict:
    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=_system_prompt(),
        tools=TOOLS,
        messages=[{"role": "user", "content": text}],
    )

    reply = " ".join(
        block.text.strip() for block in response.content if block.type == "text" and block.text.strip()
    )

    tool_use = next((block for block in response.content if block.type == "tool_use"), None)

    if tool_use is None:
        return {
            "action": "none",
            "title": None,
            "due_date": None,
            "notes": None,
            "reply": reply or "Ainda não sei fazer isso.",
        }

    args = tool_use.input
    title = args.get("title")
    return {
        "action": "create_reminder",
        "title": title,
        "due_date": args.get("due_date"),
        "notes": args.get("notes"),
        "reply": reply or f"Ok, vou te lembrar de {title}.",
    }
