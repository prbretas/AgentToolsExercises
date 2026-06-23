"""
🔬 Seção 4 — Modo Manual: Inspecionando o Tool Call
Força o modelo a gerar um tool call (sem executar) e imprime nome + argumentos.

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

# ── Tools (só precisam existir como funções com docstring) ────────────────────
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


# ── Helper com retry ──────────────────────────────────────────────────────────
def gemini_generate(contents, tools=None, tool_config=None):
    config_kwargs = {}
    if tools:
        config_kwargs["tools"] = tools
    if tool_config:
        config_kwargs["tool_config"] = tool_config
    config = types.GenerateContentConfig(**config_kwargs) if config_kwargs else None

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


# ── Inspeciona o tool call sem executá-lo ─────────────────────────────────────
print(f"\n{'='*60}")
print("SEÇÃO 4: Inspecionando o Tool Call (sem executar)")
print(f"{'='*60}")

response_manual = gemini_generate(
    contents=f"Hoje é {date.today().strftime('%d/%m/%Y')} (timezone -03:00). O que tenho hoje?",
    tools=[list_events, create_event],
    tool_config=types.ToolConfig(
        function_calling_config=types.FunctionCallingConfig(mode="ANY")
    )
)

encontrou = False
for part in response_manual.candidates[0].content.parts:
    if part.function_call:
        encontrou = True
        print("  Tool :", part.function_call.name)
        print("  Args :", dict(part.function_call.args))

if not encontrou:
    print("  (nenhum tool call encontrado na resposta)")

print("\n✅ Seção 4 OK!")
