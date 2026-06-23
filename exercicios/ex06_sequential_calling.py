"""
🌦️ Seção 6 — Sequential Function Calling: Cidade → Coordenadas → Clima
O Gemini encadeia get_city_coordinates → get_weather automaticamente.

Requer: pip install google-genai requests
"""

import re
import time
import requests
import certifi
import urllib3
from google import genai
from google.genai import types
from google.genai import errors as genai_errors

import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
SSL_VERIFY = False

# ── Config ────────────────────────────────────────────────────────────────────
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
client = genai.Client(
    api_key=GOOGLE_API_KEY,
    http_options={"verify_ssl": False}
)
print("✅ Gemini configurado!")


# ── Tools ─────────────────────────────────────────────────────────────────────
def get_city_coordinates(city_name: str) -> dict:
    """Retorna latitude e longitude de uma cidade pelo nome (via OpenStreetMap)."""
    try:
        r = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": city_name, "format": "json", "limit": 1},
            headers={"User-Agent": "lab365-ia-devs/1.0"},
            timeout=5,
            verify=SSL_VERIFY
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
            timeout=5,
            verify=SSL_VERIFY
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


TOOLS_MAP = {"get_city_coordinates": get_city_coordinates, "get_weather": get_weather}

# ── Helper com retry ──────────────────────────────────────────────────────────
def gemini_generate(contents, tools):
    config = types.GenerateContentConfig(tools=tools)
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


def run_agent_seq(prompt: str) -> str:
    """Loop de function calling para as tools de clima."""
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
            fn = TOOLS_MAP.get(fc.name)
            result = fn(**dict(fc.args)) if fn else {"error": "não encontrada"}
            print(f"  🔧 Tool: {fc.name}({dict(fc.args)}) → {result}")
            tool_results.append(
                types.Part(function_response=types.FunctionResponse(
                    name=fc.name, response={"result": result}
                ))
            )
        contents.append(types.Content(role="user", parts=tool_results))
    return "(sem resposta final)"


# ── Execução ──────────────────────────────────────────────────────────────────
print(f"\n{'='*60}")
print("SEÇÃO 6: Clima em Florianópolis (encadeamento de tools)")
print(f"{'='*60}")

resposta = run_agent_seq("Qual a temperatura atual em Florianópolis?")
print(resposta)

print("\n✅ Seção 6 OK!")
