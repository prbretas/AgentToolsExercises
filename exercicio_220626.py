"""
🤖 Aula 1 — Tool-Use: Function Calling Nativo com Python
IA para DEVs | LAB 365 / aSCTI.SC | Módulo 2 · Semana 03
Rodando localmente — SDK google-genai (novo)
"""

# pip install google-genai openai requests

import requests
import json
import time
import re
from datetime import datetime, date
from google import genai
from google.genai import types
from google.genai import errors as genai_errors

# ─── 🔐 1. API Keys ───────────────────────────────────────────────────────────
import os
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
GROQ_API_KEY   = os.getenv("GROQ_API_KEY", "")

client = genai.Client(api_key=GOOGLE_API_KEY)
print("✅ Gemini configurado!")


def gemini_generate(contents, tools=None, tool_config=None):
    """Wrapper com retry automático em caso de rate limit (429)."""
    config_kwargs = {}
    if tools:
        config_kwargs["tools"] = tools
    if tool_config:
        config_kwargs["tool_config"] = tool_config

    for attempt in range(5):
        try:
            return client.models.generate_content(
                model="gemini-2.5-flash",
                contents=contents,
                config=types.GenerateContentConfig(**config_kwargs) if config_kwargs else None
            )
        except genai_errors.ClientError as e:
            if e.code == 429:
                # Extrai o tempo de retry sugerido pela API
                wait = 30
                match = re.search(r'retry in (\d+)', str(e))
                if match:
                    wait = int(match.group(1)) + 5
                print(f"  ⏳ Rate limit atingido. Aguardando {wait}s... (tentativa {attempt+1}/5)")
                time.sleep(wait)
            else:
                raise
    raise RuntimeError("Rate limit persistiu após 5 tentativas.")


# ─── 🗓️ 2. Calendar Mock ──────────────────────────────────────────────────────
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
    return [
        e for e in AGENDA
        if dt_ini <= datetime.fromisoformat(e["inicio"]) <= dt_fim
    ]


def create_event(titulo: str, data_inicio: str, data_fim: str) -> dict:
    """Cria um novo evento no calendário (ISO 8601)."""
    novo = {"titulo": titulo, "inicio": data_inicio, "fim": data_fim}
    AGENDA.append(novo)
    return {"status": "criado", "titulo": titulo, "inicio": data_inicio}


# Teste manual das funções
hoje_inicio = f"{hoje}T00:00:00-03:00"
hoje_fim    = f"{hoje}T23:59:59-03:00"
print(f"\n📅 Eventos hoje (teste direto): {list_events(hoje_inicio, hoje_fim)}")


# ─── Helper: executa o loop de function calling manualmente ──────────────────
TOOLS_MAP = {
    "list_events":  list_events,
    "create_event": create_event,
}

def run_agent(prompt: str, tools: list, label: str = "") -> str:
    """Executa o loop de function calling até o modelo retornar texto final."""
    if label:
        print(f"\n{'='*60}\n{label}\n{'='*60}")

    contents = [types.Content(role="user", parts=[types.Part(text=prompt)])]

    for _ in range(10):  # máx 10 rodadas para evitar loop infinito
        response = gemini_generate(contents, tools=tools)

        candidate = response.candidates[0]
        parts = candidate.content.parts

        # Coleta todos os function_calls desta rodada
        fn_calls = [p for p in parts if p.function_call is not None]
        text_parts = [p for p in parts if p.text]

        # Se não há tool calls, o modelo respondeu com texto — fim
        if not fn_calls:
            return "\n".join(p.text for p in text_parts)

        # Adiciona a resposta do modelo ao histórico
        contents.append(candidate.content)

        # Executa cada tool call e coleta os resultados
        tool_results = []
        for part in fn_calls:
            fc = part.function_call
            fn = TOOLS_MAP.get(fc.name)
            if fn:
                args = dict(fc.args)
                result = fn(**args)
                print(f"  🔧 Tool chamada: {fc.name}({args}) → {result}")
            else:
                result = {"error": f"Função {fc.name} não encontrada"}

            tool_results.append(
                types.Part(
                    function_response=types.FunctionResponse(
                        name=fc.name,
                        response={"result": result}
                    )
                )
            )

        # Devolve os resultados ao modelo
        contents.append(types.Content(role="user", parts=tool_results))

    return "(loop encerrado sem resposta final)"


# ─── 🤖 3. Automatic Function Calling ────────────────────────────────────────
tools_agenda = [list_events, create_event]

resposta1 = run_agent(
    prompt=f"Hoje é {date.today().strftime('%d/%m/%Y')} (timezone -03:00). O que tenho na minha agenda hoje?",
    tools=tools_agenda,
    label="PERGUNTA 1: O que tenho hoje?"
)
print(resposta1)

resposta2 = run_agent(
    prompt=(
        f"Hoje é {date.today().strftime('%d/%m/%Y')} (timezone -03:00). "
        "Há 1 hora livre entre 14h e 18h? Se sim, crie um evento chamado 'Sprint Review' "
        "nesse horário livre com duração de 1 hora. Use o timezone -03:00."
    ),
    tools=tools_agenda,
    label="PERGUNTA 2: Agendar Sprint Review se houver horário livre"
)
print(resposta2)

# ─── 🔬 4. Modo Manual: Inspecionando o Tool Call ─────────────────────────────
print(f"\n{'='*60}")
print("SEÇÃO 4: Inspecionando o Tool Call manualmente (sem executar)")
print(f"{'='*60}")

response_manual = gemini_generate(
    contents=f"Hoje é {date.today().strftime('%d/%m/%Y')} (timezone -03:00). O que tenho hoje?",
    tools=[list_events, create_event],
    tool_config=types.ToolConfig(
        function_calling_config=types.FunctionCallingConfig(mode="ANY")
    )
)

for part in response_manual.candidates[0].content.parts:
    if part.function_call:
        print("Tool:", part.function_call.name)
        print("Args:", dict(part.function_call.args))

# ─── 🔌 5. Portabilidade: Groq com SDK OpenAI ────────────────────────────────
print(f"\n{'='*60}")
print("SEÇÃO 5: Groq com SDK OpenAI")
print(f"{'='*60}")

try:
    from openai import OpenAI

    client_groq = OpenAI(
        api_key=GROQ_API_KEY,
        base_url="https://api.groq.com/openai/v1"
    )

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

    resp = client_groq.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{
            "role": "user",
            "content": f"Hoje é {date.today().strftime('%d/%m/%Y')} (timezone -03:00). O que tenho hoje na agenda?"
        }],
        tools=tools_schema,
        tool_choice="auto"
    )

    print("finish_reason:", resp.choices[0].finish_reason)
    if resp.choices[0].finish_reason == "tool_calls":
        tc = resp.choices[0].message.tool_calls[0]
        print("Tool:", tc.function.name)
        print("Args:", tc.function.arguments)

except Exception as e:
    print(f"⚠️ Groq erro: {e}")

# ─── 🌦️ 6. Sequential Function Calling ───────────────────────────────────────
print(f"\n{'='*60}")
print("SEÇÃO 6: Sequential Function Calling — Clima em Florianópolis")
print(f"{'='*60}")

def get_city_coordinates(city_name: str) -> dict:
    """Retorna latitude e longitude de uma cidade pelo nome (via OpenStreetMap)."""
    try:
        r = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": city_name, "format": "json", "limit": 1},
            headers={"User-Agent": "lab365-ia-devs/1.0"},
            timeout=5
        )
        r.raise_for_status()
        data = r.json()
        if not data:
            return {"error": "Cidade não encontrada"}
        return {"lat": float(data[0]["lat"]), "lon": float(data[0]["lon"]), "nome": data[0]["display_name"]}
    except Exception as e:
        return {"error": str(e)}


def get_weather(latitude: float, longitude: float) -> dict:
    """Retorna temperatura atual e velocidade do vento para as coordenadas informadas."""
    try:
        r = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,wind_speed_10m"
            },
            timeout=5
        )
        r.raise_for_status()
        data = r.json()
        current = data.get("current", {})
        return {
            "temperatura_celsius": current.get("temperature_2m"),
            "vento_kmh": current.get("wind_speed_10m"),
            "status": "ok"
        }
    except Exception as e:
        return {"error": str(e)}


# Loop manual para seção 6
TOOLS_MAP_SEQ = {
    "get_city_coordinates": get_city_coordinates,
    "get_weather": get_weather,
}

def run_agent_seq(prompt: str) -> str:
    contents = [types.Content(role="user", parts=[types.Part(text=prompt)])]
    for _ in range(10):
        response = gemini_generate(contents, tools=[get_city_coordinates, get_weather])
        candidate = response.candidates[0]
        parts = candidate.content.parts
        fn_calls = [p for p in parts if p.function_call is not None]
        if not fn_calls:
            return "\n".join(p.text for p in parts if p.text)
        contents.append(candidate.content)
        tool_results = []
        for part in fn_calls:
            fc = part.function_call
            fn = TOOLS_MAP_SEQ.get(fc.name)
            result = fn(**dict(fc.args)) if fn else {"error": "não encontrada"}
            print(f"  🔧 Tool: {fc.name}({dict(fc.args)}) → {result}")
            tool_results.append(
                types.Part(
                    function_response=types.FunctionResponse(
                        name=fc.name,
                        response={"result": result}
                    )
                )
            )
        contents.append(types.Content(role="user", parts=tool_results))
    return "(sem resposta)"

print(run_agent_seq("Qual a temperatura atual em Florianópolis?"))


# ─── 🛡️ 7. Tool Robusta ───────────────────────────────────────────────────────
print(f"\n{'='*60}")
print("SEÇÃO 7: Tool Robusta — Tratamento de Erros")
print(f"{'='*60}")

def get_weather_robusto(latitude: float, longitude: float) -> dict:
    """Versão robusta: valida input, timeout, trata erros sem quebrar o agente."""
    if not (-90 <= latitude <= 90):
        return {"error": f"Latitude inválida: {latitude}. Deve estar entre -90 e 90."}
    if not (-180 <= longitude <= 180):
        return {"error": f"Longitude inválida: {longitude}. Deve estar entre -180 e 180."}
    try:
        r = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,wind_speed_10m"
            },
            timeout=5
        )
        r.raise_for_status()
        data = r.json()
        if "current" not in data:
            return {"error": "Resposta da API sem campo 'current'"}
        current = data["current"]
        return {
            "temperatura_celsius": current.get("temperature_2m"),
            "vento_kmh": current.get("wind_speed_10m"),
            "status": "ok"
        }
    except requests.Timeout:
        return {"error": "Timeout ao consultar a API de clima (>5s)"}
    except requests.HTTPError as e:
        return {"error": f"Erro HTTP {e.response.status_code}: {str(e)}"}
    except Exception as e:
        return {"error": f"Erro inesperado: {str(e)}"}


print("Latitude inválida:", get_weather_robusto(200, 0))
print("Normal (Florianópolis):", get_weather_robusto(-27.5954, -48.5480))

print("\n✅ Exercício concluído!")
