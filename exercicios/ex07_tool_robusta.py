"""
🛡️ Seção 7 — Tool Robusta: Tratamento de Erros
Testa get_weather_robusto com casos válidos e inválidos — sem chamar nenhuma API de IA.

Requer: pip install requests
"""

import ssl
import certifi
import urllib3
import requests

# Suprime warnings de SSL em redes corporativas com proxy self-signed
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
SSL_VERIFY = False  # mude para certifi.where() fora de rede corporativa

# ── Tool ──────────────────────────────────────────────────────────────────────
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
            timeout=5,
            verify=SSL_VERIFY
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


# ── Testes ────────────────────────────────────────────────────────────────────
print(f"{'='*60}")
print("SEÇÃO 7: Tool Robusta — Casos de Teste")
print(f"{'='*60}\n")

casos = [
    ("Latitude inválida (200)",     200,       0),
    ("Longitude inválida (-200)",    -27.5954, -200),
    ("Florianópolis (válido)",       -27.5954, -48.5480),
    ("São Paulo (válido)",           -23.5505, -46.6333),
    ("Londres (válido)",             51.5074,  -0.1278),
     ("Joinville",                  -26.304516,  -48.843380),
]

for descricao, lat, lon in casos:
    resultado = get_weather_robusto(lat, lon)
    status = "✅" if "error" not in resultado else "⚠️ "
    print(f"{status} {descricao}")
    print(f"   → {resultado}\n")

print("✅ Seção 7 OK!")
