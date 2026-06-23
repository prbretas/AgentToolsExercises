"""
🤖 Seção 3 — Automatic Function Calling com Gemini
O agente chama list_events e create_event automaticamente.

Requer: pip install google-genai
"""

import re
import time
from datetime import datetime, date
import httpx
from google import genai
from google.genai import types
from google.genai import errors as genai_errors

import os

# ── Config ────────────────────────────────────────────────────────────────────
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
client = genai.Client(
    api_key=GOOGLE_API_KEY,
    http_options={"verify_ssl": False}
)
print("✅ Gemini configurado!")

# ── Agenda mock ───────────────────────────────────────────────────────────────
hoje = date.today().isoformat()

AGENDA = [
    {"titulo": "Daily Scrum",       "inicio": f"{hoje}T09:00:00-03:00", "fim": f"{hoje}T09:30:00-03:00"},
    {"titulo": "Revisão de código", "inicio": f"{hoje}T11:00:00-03:00", "fim": f"{hoje}T12:00:00-03:00"},
    {"titulo": "Almoço com equipe", "inicio": f"{hoje}T12:30:00-03:00", "fim": f"{hoje}T13:30:00-03:00"},
]


def list_events(data_inicio: str, data_fim: str) -> list:
    """Lista eventos do calendário entre duas datas (ISO 8601)."""
    dt_ini = datetime.fromisoformat(data_inicio)
    dt_fim = datetime.fromisoformat(data_fim)
    return [e for e in AGENDA if dt_ini <= datetime.fromisoformat(e["inicio"]) <= dt_fim]


def create_event(titulo: str, data_inicio: str, data_fim: str) -> dict:
    """Cria um novo evento no calendário (ISO 8601)."""
    novo = {"titulo": titulo, "inicio": data_inicio, "fim": data_fim}
    AGENDA.append(novo)
    return {"status": "criado", "titulo": titulo, "inicio": data_inicio}


TOOLS_MAP = {"list_events": list_events, "create_event": create_event}

# ── Helper com retry ──────────────────────────────────────────────────────────
def gemini_generate(contents, tools=None):
    config = types.GenerateContentConfig(tools=tools) if tools else None
    for attempt in range(8):
        try:
            return client.models.generate_content(
                model="gemini-2.0-flash-lite",
                contents=contents,
                config=config
            )
        except genai_errors.ClientError as e:
            if e.code == 429:
                wait = 30
                m = re.search(r'retry in (\d+)', str(e))
                if m:
                    wait = int(m.group(1)) + 5
                print(f"  ⏳ Rate limit. Aguardando {wait}s... (tentativa {attempt+1}/8)")
                time.sleep(wait)
            else:
                raise
    raise RuntimeError("Rate limit persistiu.")


def run_agent(prompt: str, label: str = ""):
    """Loop de function calling até o modelo retornar texto final."""
    if label:
        print(f"\n{'='*60}\n{label}\n{'='*60}")

    contents = [types.Content(role="user", parts=[types.Part(text=prompt)])]

    for _ in range(10):
        response = gemini_generate(contents, tools=[list_events, create_event])
        candidate = response.candidates[0]
        parts = candidate.content.parts

        fn_calls = [p for p in parts if p.function_call is not None]

        if not fn_calls:
            return "\n".join(p.text for p in parts if p.text)

        contents.append(candidate.content)

        tool_results = []
        for part in fn_calls:
            fc = part.function_call
            fn = TOOLS_MAP.get(fc.name)
            result = fn(**dict(fc.args)) if fn else {"error": f"{fc.name} não encontrada"}
            print(f"  🔧 Tool: {fc.name}({dict(fc.args)}) → {result}")
            tool_results.append(
                types.Part(function_response=types.FunctionResponse(
                    name=fc.name, response={"result": result}
                ))
            )
        contents.append(types.Content(role="user", parts=tool_results))

    return "(loop encerrado sem resposta final)"


# ── Pergunta 1 ────────────────────────────────────────────────────────────────
resposta1 = run_agent(
    prompt=f"Hoje é {date.today().strftime('%d/%m/%Y')} (timezone -03:00). O que tenho na agenda hoje?",
    label="PERGUNTA 1: O que tenho hoje?"
)
print(resposta1)

# ── Pergunta 2 ────────────────────────────────────────────────────────────────
resposta2 = run_agent(
    prompt=(
        f"Hoje é {date.today().strftime('%d/%m/%Y')} (timezone -03:00). "
        "Há 1 hora livre entre 14h e 18h? Se sim, crie um evento chamado 'Sprint Review' "
        "com 1 hora de duração nesse horário. Use timezone -03:00."
    ),
    label="PERGUNTA 2: Agendar Sprint Review se houver horário livre"
)
print(resposta2)

print("\n✅ Seção 3 OK!")
