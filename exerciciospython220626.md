🤖 Aula 1 — Tool-Use: Function Calling Nativo com Python — Exercício do Aluno
IA para DEVs | LAB 365 / aSCTI.SC | Módulo 2 · Semana 03
Objetivo: Entender o fluxo de function calling nas três principais APIs (OpenAI, Anthropic, Gemini) e construir um assistente de agenda funcional.

Stack: Google Gemini Flash · Groq (Llama 3.3 70B) · Calendar Mock · Open-Meteo

💡 Como usar: Preencha cada bloco # TODO: e execute antes de avançar.

📦 0. Instalação de dependências
Execute e aguarde — não precisa alterar nada aqui.

!pip install -q google-generativeai openai smolagents requests
print('✅ Dependências instaladas!')
✅ Dependências instaladas!


🔐 1. Configurar Gemini
Adicione sua chave em: Colab → ícone 🔑 → Secrets → GOOGLE_API_KEY
Obtenha em: https://aistudio.google.com → Get API Key

from google.colab import userdata
import google.generativeai as genai

GOOGLE_API_KEY = userdata.get('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
print('✅ Gemini configurado!')
✅ Gemini configurado!
🗓️ 2. Calendar Mock
Em vez de conectar na API real do Google Calendar (que exige OAuth complexo),
usamos uma lista Python que simula uma agenda real.
O function calling funciona exatamente igual — só o backend muda.

💡 Didática: Isso é o mesmo padrão da inbox.json da Aula 2.
Aprenda o mecanismo primeiro, integre sistemas reais depois.

from datetime import datetime, date

TZ = 'America/Sao_Paulo'

# Agenda simulada — adicione ou remova eventos à vontade!
AGENDA = [
    # TODO: adicione pelo menos 3 eventos com datas de hoje e amanhã
    # Formato: {'titulo': str, 'inicio': 'YYYY-MM-DDTHH:MM:SS-03:00', 'fim': 'YYYY-MM-DDTHH:MM:SS-03:00'}
]

# TODO: implemente list_events — filtre AGENDA pelo intervalo data_inicio/data_fim
def list_events(data_inicio: str, data_fim: str) -> list:
    """
    Lista eventos do calendário entre duas datas.
    As datas devem estar em formato ISO 8601, ex: '2026-06-23T00:00:00-03:00'
    """
    # Dica: converta data_inicio e data_fim para datetime e compare com cada evento
    # from datetime import datetime
    # dt_ini = datetime.fromisoformat(data_inicio)
    # dt_fim = datetime.fromisoformat(data_fim)
    # return [e for e in AGENDA if dt_ini <= datetime.fromisoformat(e['inicio']) <= dt_fim]
    pass


# TODO: implemente create_event — adicione o evento em AGENDA e retorne confirmação
def create_event(titulo: str, data_inicio: str, data_fim: str) -> dict:
    """
    Cria um novo evento no calendário.
    As datas devem estar em formato ISO 8601, ex: '2026-06-23T14:00:00-03:00'
    """
    # Dica:
    # novo = {'titulo': titulo, 'inicio': data_inicio, 'fim': data_fim}
    # AGENDA.append(novo)
    # return {'status': 'criado', 'titulo': titulo, 'inicio': data_inicio}
    pass


# TODO: teste manual — chame list_events com o intervalo de hoje e imprima
hoje_inicio = f"{date.today()}T00:00:00-03:00"
hoje_fim    = f"{date.today()}T23:59:59-03:00"
# eventos = list_events(hoje_inicio, hoje_fim)
# print(f'Eventos hoje: {eventos}')

🤖 3. Assistente com Automatic Function Calling
O Gemini executa o loop de tool-call automaticamente.
Basta passar as funções Python diretamente como tools.


# TODO: crie o modelo Gemini passando list_events e create_event como tools
# model = genai.GenerativeModel(
#     model_name='gemini-2.5-flash',
#     tools=[list_events, create_event]
# )

# ─── Pergunta 1: O que tenho hoje? ───────────────────────────────────────────
print('=' * 60)
print('PERGUNTA 1: O que tenho hoje?')
print('=' * 60)

# TODO: chame model.generate_content() perguntando o que há na agenda hoje
# Dica: inclua date.today() na pergunta para o modelo saber a data
# response = model.generate_content(...)
# print(response.text)

============================================================
PERGUNTA 1: O que tenho hoje?
============================================================

# ─── Pergunta 2: Agendar se houver slot livre ────────────────────────────────
print('=' * 60)
print('PERGUNTA 2: Agendar Sprint Review se houver horário livre')
print('=' * 60)

# TODO: pergunte se há 1h livre entre 14h e 18h e peça para criar 'Sprint Review'
# Lembre de incluir a data de hoje e mencionar o timezone -03:00
# response = model.generate_content(...)
# print(response.text)

============================================================
PERGUNTA 2: Agendar Sprint Review se houver horário livre
============================================================
🔬 4. Modo Manual: Inspecionando o Tool Call
Desative o Automatic Function Calling para ver o que o modelo gera
antes de executar a tool — nome da função e argumentos brutos.

from google.generativeai import types

model_manual = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    tools=[list_events, create_event]
)

# TODO: chame generate_content com tool_config Mode.ANY para forçar tool call
# response_manual = model_manual.generate_content(
#     f'Hoje é {date.today().strftime("%d/%m/%Y")}. O que tenho hoje?',
#     tool_config=types.ToolConfig(
#         function_calling_config=types.FunctionCallingConfig(
#             mode=types.FunctionCallingConfig.Mode.ANY
#         )
#     )
# )

# TODO: itere sobre response_manual.candidates[0].content.parts
# e imprima o nome da função e os argumentos
# for part in ...:
#     if hasattr(part, 'function_call'):
#         print('Tool:', part.function_call.name)
#         print('Args:', dict(part.function_call.args))

🔌 5. Portabilidade: Groq com SDK OpenAI
O mesmo código funciona em qualquer provedor OpenAI-compatible.
Só muda 2 linhas!

Adicione GROQ_API_KEY em Colab → Secrets. Obtenha em https://console.groq.com


try:
    GROQ_API_KEY = userdata.get('GROQ_API_KEY')
    from openai import OpenAI

    # TODO: preencha as 2 linhas que mudam para usar Groq
    client_groq = OpenAI(
        api_key=...,    # TODO: use GROQ_API_KEY
        base_url=...    # TODO: 'https://api.groq.com/openai/v1'
    )

    # Schema da tool (padrão OpenAI)
    tools_schema = [{
        'type': 'function',
        'function': {
            'name': 'list_events',
            'description': 'Lista eventos do calendário entre duas datas.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'data_inicio': {'type': 'string', 'description': 'Data início ISO 8601'},
                    'data_fim':    {'type': 'string', 'description': 'Data fim ISO 8601'}
                },
                'required': ['data_inicio', 'data_fim']
            }
        }
    }]

    # TODO: chame client_groq.chat.completions.create() com o schema acima
    # model='llama-3.3-70b-versatile', tool_choice='auto'
    # resp = client_groq.chat.completions.create(...)

    # TODO: imprima finish_reason, nome da tool e os argumentos
    # print('finish_reason:', resp.choices[0].finish_reason)
    # if resp.choices[0].finish_reason == 'tool_calls':
    #     tc = resp.choices[0].message.tool_calls[0]
    #     print('Tool:', tc.function.name)
    #     print('Args:', tc.function.arguments)

except Exception as e:
    print(f'⚠️ Groq não configurado: {e}')

⚠️ Groq não configurado: Invalid type for url.  Expected str or httpx.URL, got <class 'ellipsis'>: Ellipsis
🌦️ 6. Sequential Function Calling: Cidade → Coordenadas → Clima
O Gemini encadeia tools automaticamente quando os outputs de uma
são o input da próxima — sem nenhum código extra.


import requests

def get_city_coordinates(city_name: str) -> dict:
    """Retorna latitude e longitude de uma cidade pelo nome (via OpenStreetMap)."""
    # TODO: faça GET em 'https://nominatim.openstreetmap.org/search'
    # params: {'q': city_name, 'format': 'json', 'limit': 1}
    # headers: {'User-Agent': 'lab365-ia-devs/1.0'}, timeout=5
    # Retorne {'lat': float, 'lon': float, 'nome': str}
    # Se não encontrar: {'error': 'Cidade não encontrada'}
    pass


def get_weather(latitude: float, longitude: float) -> dict:
    """Retorna temperatura atual e velocidade do vento para as coordenadas informadas."""
    # TODO: faça GET em 'https://api.open-meteo.com/v1/forecast'
    # params: latitude, longitude, current='temperature_2m,wind_speed_10m'
    # Retorne {'temperatura_celsius': float, 'vento_kmh': float, 'status': 'ok'}
    pass


# TODO: crie GenerativeModel com as duas tools e pergunte a temperatura em Florianópolis
# model_seq = genai.GenerativeModel('gemini-2.5-flash', tools=[get_city_coordinates, get_weather])
# response = model_seq.generate_content('Qual a temperatura atual em Florianópolis?')
# print(response.text)

🛡️ 7. Tool Robusta: Tratamento de Erros
Regra de ouro: a tool NUNCA deve quebrar o loop do agente.
Sempre retorne um dict — inclusive em caso de erro.

Três camadas de proteção: validação de input · timeout explícito · try/except completo


def get_weather_robusto(latitude: float, longitude: float) -> dict:
    """Versão robusta: valida input, timeout, trata erros sem quebrar o agente."""

    # TODO 1: valide latitude (-90 a 90) — retorne {'error': '...'} se inválida

    # TODO 2: valide longitude (-180 a 180) — retorne {'error': '...'} se inválida

    try:
        # TODO 3: GET com timeout=5 e r.raise_for_status()

        # TODO 4: valide que 'current' existe na resposta

        # TODO 5: retorne {'temperatura_celsius': ..., 'vento_kmh': ..., 'status': 'ok'}
        pass

    except requests.Timeout:
        # TODO 6: retorne dict de erro de timeout
        pass
    except requests.HTTPError as e:
        # TODO 7: retorne dict com código HTTP
        pass
    except Exception as e:
        # TODO 8: retorne dict de erro genérico
        pass


# Testes
print('Latitude inválida:', get_weather_robusto(200, 0))
print('Normal (Florianópolis):', get_weather_robusto(-27.5954, -48.5480))

Latitude inválida: None
Normal (Florianópolis): None
🏋️ Exercício Final
Entregável:

✅ AGENDA com pelo menos 3 eventos de hoje
✅ list_events e create_event funcionando
✅ Agente criou pelo menos 1 evento via linguagem natural
✅ Print do tool call inspecionado (seção 4)
Desafio extra:

Adicione uma 3ª tool delete_event(titulo: str) que remove da AGENDA
Implemente human-in-the-loop: antes de create_event, peça confirmação via input()
Use get_weather_robusto como tool e combine com a agenda: 'Está chovendo? Se sim, mova a reunião externa para online'