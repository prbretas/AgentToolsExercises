"""
🔌 Seção 5 — Portabilidade: Groq com SDK OpenAI
Mesma interface OpenAI, só muda api_key e base_url.

Requer: pip install openai httpx
"""

import warnings
import urllib3
from datetime import date
import httpx
from openai import OpenAI

import os

# Suprime warnings de SSL (necessário em redes corporativas com proxy self-signed)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings("ignore")

# ── Config ────────────────────────────────────────────────────────────────────
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Passa httpx.Client com verify=False para contornar proxy corporativo
http_client = httpx.Client(verify=False)

client_groq = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
    http_client=http_client
)
print("✅ Groq configurado!")

# ── Schema da tool ────────────────────────────────────────────────────────────
tools_schema = [{
    "type": "function",
    "function": {
        "name": "list_events",
        "description": "Lista eventos do calendário entre duas datas.",
        "parameters": {
            "type": "object",
            "properties": {
                "data_inicio": {"type": "string", "description": "Data início ISO 8601"},
                "data_fim":    {"type": "string", "description": "Data fim ISO 8601"}
            },
            "required": ["data_inicio", "data_fim"]
        }
    }
}]

# ── Chamada ───────────────────────────────────────────────────────────────────
print(f"\n{'='*60}")
print("SEÇÃO 5: Groq — tool call via Llama 3.3 70B")
print(f"{'='*60}")

resp = client_groq.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{
        "role": "user",
        "content": f"Hoje é {date.today().strftime('%d/%m/%Y')} (timezone -03:00). O que tenho hoje na agenda?"
    }],
    tools=tools_schema,
    tool_choice="auto"
)

print("finish_reason :", resp.choices[0].finish_reason)

if resp.choices[0].finish_reason == "tool_calls":
    tc = resp.choices[0].message.tool_calls[0]
    print("Tool          :", tc.function.name)
    print("Args          :", tc.function.arguments)
else:
    print("Resposta texto:", resp.choices[0].message.content)

print("\n✅ Seção 5 OK!")
