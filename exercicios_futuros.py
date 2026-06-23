"""
🚀 10 Exercícios Futuros — Agentes e Tools com Python
IA para DEVs | LAB 365 / aSCTI.SC

Cada exercício tem:
  - Conceito central
  - Esqueleto com TODO para preencher
  - Testes que mostram o resultado esperado

Rode cada seção individualmente comentando/descomentando o bloco desejado.

Dependências por exercício:
  pip install google-genai openai requests httpx duckduckgo-search
"""

# =============================================================================
# EXERCÍCIO 1 — Tool com Memória: Agente de Notas Pessoais
# =============================================================================
"""
CONCEITO: Estado persistente entre tool calls.
O agente mantém um "bloco de notas" em memória. Você pode pedir para
salvar, listar e deletar notas via linguagem natural.

SKILLS: create_tool, stateful_tool, multi-turn
"""

# notes_db: dict[str, str] = {}
#
# def save_note(titulo: str, conteudo: str) -> dict:
#     """Salva uma nota com título e conteúdo."""
#     # TODO: salve em notes_db e retorne confirmação
#     pass
#
# def list_notes() -> list:
#     """Lista todos os títulos de notas salvas."""
#     # TODO: retorne lista de títulos
#     pass
#
# def get_note(titulo: str) -> dict:
#     """Recupera o conteúdo de uma nota pelo título."""
#     # TODO: busque em notes_db, retorne {"titulo": ..., "conteudo": ...}
#     # Se não existir: {"error": f"Nota '{titulo}' não encontrada"}
#     pass
#
# def delete_note(titulo: str) -> dict:
#     """Remove uma nota pelo título."""
#     # TODO: delete de notes_db
#     pass
#
# # TESTES ESPERADOS:
# # save_note("Reunião", "Falar sobre deploy")  → {"status": "salva", "titulo": "Reunião"}
# # list_notes()                                → ["Reunião"]
# # get_note("Reunião")                         → {"titulo": "Reunião", "conteudo": "Falar sobre deploy"}
# # delete_note("Reunião")                      → {"status": "removida", "titulo": "Reunião"}
# # get_note("Reunião")                         → {"error": "Nota 'Reunião' não encontrada"}
#
# # PROMPT DE TESTE PARA O AGENTE:
# # "Salva uma nota chamada 'ideias' com o texto 'usar Redis como cache'.
# #  Depois me diz o que está escrito nessa nota."


# =============================================================================
# EXERCÍCIO 2 — Human-in-the-Loop: Agente com Confirmação
# =============================================================================
"""
CONCEITO: O agente pede aprovação humana antes de executar ações destrutivas.
Antes de deletar ou enviar qualquer coisa, o agente pergunta ao usuário.

SKILLS: human_in_the_loop, input(), tool_wrapper, safety
"""

# def delete_event_com_confirmacao(titulo: str) -> dict:
#     """Remove um evento da agenda após confirmação do usuário."""
#     # TODO 1: print f"⚠️ Tem certeza que quer deletar '{titulo}'? (s/n)"
#     # TODO 2: use input() para capturar resposta
#     # TODO 3: se resposta == 's': remova e retorne {"status": "removido"}
#     # TODO 4: caso contrário: retorne {"status": "cancelado"}
#     pass
#
# # TESTES ESPERADOS:
# # Usuário digita 's' → {"status": "removido", "titulo": "Daily Scrum"}
# # Usuário digita 'n' → {"status": "cancelado"}
#
# # PROMPT DE TESTE PARA O AGENTE:
# # "Delete o evento 'Daily Scrum' da minha agenda de hoje."


# =============================================================================
# EXERCÍCIO 3 — Multi-Tool Pipeline: Pesquisa + Resumo
# =============================================================================
"""
CONCEITO: Agente usa DuckDuckGo para buscar na web e depois resume o resultado.
Demonstra como conectar ferramentas de dados externos a LLMs.

SKILLS: web_search_tool, summarization, pipeline
Dependência extra: pip install duckduckgo-search
"""

# from duckduckgo_search import DDGS
#
# def buscar_web(query: str, max_resultados: int = 3) -> list:
#     """Busca na web usando DuckDuckGo e retorna títulos + snippets."""
#     # TODO: use DDGS().text(query, max_results=max_resultados)
#     # Retorne lista de {"titulo": ..., "url": ..., "snippet": ...}
#     # Se erro: retorne [{"error": str(e)}]
#     pass
#
# # TESTES ESPERADOS:
# # buscar_web("Python function calling LLM")
# # → [{"titulo": "...", "url": "https://...", "snippet": "..."},  ...]
#
# # PROMPT DE TESTE PARA O AGENTE:
# # "Pesquise sobre 'LangChain vs LlamaIndex 2025' e me dê um resumo
# #  dos principais pontos encontrados."


# =============================================================================
# EXERCÍCIO 4 — Agente de Calculadora Financeira
# =============================================================================
"""
CONCEITO: Tools matemáticas compostas. O agente resolve problemas financeiros
usando múltiplas funções especializadas encadeadas.

SKILLS: math_tools, chaining, structured_output
"""

# def calcular_juros_compostos(principal: float, taxa_anual: float, anos: int) -> dict:
#     """Calcula montante final com juros compostos. Taxa em % ao ano."""
#     # TODO: montante = principal * (1 + taxa_anual/100) ** anos
#     # Retorne {"principal": ..., "montante": ..., "juros_ganhos": ..., "anos": ...}
#     pass
#
# def calcular_parcela_financiamento(valor: float, taxa_mensal: float, meses: int) -> dict:
#     """Calcula parcela mensal de financiamento (Tabela Price)."""
#     # TODO: formula Price: P = V * (i*(1+i)^n) / ((1+i)^n - 1)
#     # onde i = taxa_mensal/100, n = meses, V = valor
#     # Retorne {"valor_financiado": ..., "parcela_mensal": ..., "total_pago": ..., "juros_totais": ...}
#     pass
#
# def converter_moeda(valor: float, de: str, para: str) -> dict:
#     """Converte valor entre moedas usando taxa fixa (mock)."""
#     # TODO: crie um dict TAXAS com pelo menos USD, EUR, BRL, GBP
#     # Converta: resultado = valor / TAXAS[de] * TAXAS[para]
#     # Retorne {"valor_original": ..., "moeda_origem": ..., "valor_convertido": ..., "moeda_destino": ...}
#     pass
#
# # TESTES ESPERADOS:
# # calcular_juros_compostos(1000, 10, 5)     → montante ≈ 1610.51
# # calcular_parcela_financiamento(10000, 1, 24) → parcela ≈ 470.73
# # converter_moeda(100, "USD", "BRL")        → valor_convertido ≈ 490.0
#
# # PROMPT DE TESTE PARA O AGENTE:
# # "Se eu investir R$5.000 a 12% ao ano por 3 anos, quanto terei?
# #  E se eu financiar R$20.000 em 36 meses a 1,5% ao mês, qual a parcela?"


# =============================================================================
# EXERCÍCIO 5 — Agente com Retry e Fallback
# =============================================================================
"""
CONCEITO: Resiliência. Quando uma tool falha, o agente tenta um provider
alternativo automaticamente.

SKILLS: retry_logic, fallback_tool, error_handling, multi_provider
"""

# import requests, urllib3
# urllib3.disable_warnings()
#
# def get_weather_openmeteo(lat: float, lon: float) -> dict:
#     """Clima via Open-Meteo (provider primário)."""
#     # TODO: GET https://api.open-meteo.com/v1/forecast
#     # params: latitude, longitude, current="temperature_2m,wind_speed_10m"
#     # Retorne {"temperatura": ..., "vento": ..., "fonte": "open-meteo"}
#     pass
#
# def get_weather_wttr(cidade: str) -> dict:
#     """Clima via wttr.in (provider de fallback)."""
#     # TODO: GET f"https://wttr.in/{cidade}?format=j1" (verify=False)
#     # Extraia temp_C e windspeedKmph do JSON
#     # Retorne {"temperatura": ..., "vento": ..., "fonte": "wttr.in"}
#     pass
#
# def get_weather_com_fallback(cidade: str, lat: float, lon: float) -> dict:
#     """Tenta Open-Meteo primeiro, usa wttr.in se falhar."""
#     # TODO: tente get_weather_openmeteo, se retornar {"error": ...} tente get_weather_wttr
#     # Sempre retorne a fonte usada no dict final
#     pass
#
# # TESTES ESPERADOS:
# # get_weather_com_fallback("Florianópolis", -27.59, -48.54)
# # → {"temperatura": 16.0, "vento": 18.2, "fonte": "open-meteo"}
# # (simule falha no Open-Meteo passando lat=999 para forçar o fallback)
#
# # PROMPT DE TESTE PARA O AGENTE:
# # "Qual o clima em Curitiba agora? Use fallback se necessário."


# =============================================================================
# EXERCÍCIO 6 — Agente de Análise de CSV
# =============================================================================
"""
CONCEITO: Tools que manipulam dados estruturados. O agente analisa um CSV
e responde perguntas sobre os dados sem que você precise escrever SQL.

SKILLS: data_tools, csv_analysis, aggregation
"""

# import csv, io
# from statistics import mean, median
#
# # Dataset embutido (simula leitura de arquivo)
# CSV_VENDAS = """produto,vendas,preco,categoria
# Notebook,45,3500,Eletronicos
# Mouse,120,80,Eletronicos
# Cadeira,30,850,Moveis
# Monitor,60,1200,Eletronicos
# Mesa,15,600,Moveis
# Teclado,95,150,Eletronicos
# Headset,70,200,Eletronicos
# Estante,8,400,Moveis
# """
#
# def carregar_dados() -> list:
#     """Carrega o CSV de vendas em memória como lista de dicts."""
#     # TODO: use csv.DictReader com io.StringIO(CSV_VENDAS)
#     # Converta vendas e preco para int/float
#     # Retorne lista de dicts
#     pass
#
# def resumo_por_categoria() -> list:
#     """Retorna total de vendas e receita por categoria."""
#     # TODO: agrupe os dados por categoria
#     # Para cada categoria: {"categoria": ..., "total_vendas": ..., "receita_total": ...}
#     pass
#
# def top_produtos(n: int = 3) -> list:
#     """Retorna os N produtos com mais vendas."""
#     # TODO: ordene por vendas desc, retorne os top N
#     # {"produto": ..., "vendas": ..., "receita": ...}
#     pass
#
# def estatisticas_preco() -> dict:
#     """Retorna média, mediana, mínimo e máximo de preço."""
#     # TODO: use statistics.mean e statistics.median
#     pass
#
# # TESTES ESPERADOS:
# # top_produtos(3) → [Notebook(45), Mouse(120), Headset(70)] ordenados por vendas
# # resumo_por_categoria() → Eletronicos(390 vendas), Moveis(53 vendas)
# # estatisticas_preco()   → {"media": ..., "mediana": ..., "min": 80, "max": 3500}
#
# # PROMPT DE TESTE PARA O AGENTE:
# # "Qual categoria vendeu mais? Me dê o top 3 produtos e a média de preço."


# =============================================================================
# EXERCÍCIO 7 — Agente Multi-Etapas: Planner + Executor
# =============================================================================
"""
CONCEITO: Separar planejamento de execução. O agente primeiro cria um plano
em texto, depois executa cada passo chamando tools.

SKILLS: chain_of_thought, plan_and_execute, multi_step_agent
"""

# AGENDA_VIAGEM = []
#
# def pesquisar_voos(origem: str, destino: str, data: str) -> list:
#     """Busca voos disponíveis (mock)."""
#     # TODO: retorne lista de 2-3 voos mock com companhia, horario, preco
#     # [{"companhia": "LATAM", "horario": "08:00", "preco": 450.00}, ...]
#     pass
#
# def pesquisar_hoteis(cidade: str, checkin: str, checkout: str) -> list:
#     """Busca hotéis disponíveis (mock)."""
#     # TODO: retorne lista de 2-3 hotéis mock com nome, estrelas, preco_noite
#     pass
#
# def reservar(tipo: str, item: str, data: str) -> dict:
#     """Confirma uma reserva (voo ou hotel) e adiciona à agenda."""
#     # TODO: adicione à AGENDA_VIAGEM e retorne confirmação com código de reserva mock
#     # codigo = f"RES-{tipo[:3].upper()}-{abs(hash(item)) % 9999:04d}"
#     pass
#
# def ver_itinerario() -> list:
#     """Lista todas as reservas confirmadas."""
#     # TODO: retorne AGENDA_VIAGEM
#     pass
#
# # TESTES ESPERADOS:
# # pesquisar_voos("GRU", "FLN", "2026-07-15") → [{"companhia": ..., ...}, ...]
# # reservar("voo", "LATAM 08:00", "2026-07-15") → {"codigo": "RES-VOO-XXXX", ...}
# # ver_itinerario() → [{"tipo": "voo", "item": "LATAM 08:00", ...}]
#
# # PROMPT DE TESTE PARA O AGENTE:
# # "Quero viajar de São Paulo para Florianópolis no dia 15/07.
# #  Pesquise voos e hotéis, escolha os mais baratos e faça as reservas."


# =============================================================================
# EXERCÍCIO 8 — Agente de Monitoramento com Alertas
# =============================================================================
"""
CONCEITO: Agente que monitora métricas e decide se deve disparar alertas.
Demonstra lógica de decisão autônoma baseada em thresholds.

SKILLS: monitoring_agent, decision_making, alert_system
"""

# import random, time
# from datetime import datetime
#
# ALERTAS_DISPARADOS = []
#
# def coletar_metricas_servidor(servidor: str) -> dict:
#     """Coleta métricas de CPU, memória e disco de um servidor (mock)."""
#     # TODO: retorne valores aleatórios para simular métricas reais
#     # {"servidor": ..., "cpu_percent": random entre 10-95,
#     #  "memoria_percent": random entre 20-90, "disco_percent": random entre 30-85,
#     #  "timestamp": datetime.now().isoformat()}
#     pass
#
# def disparar_alerta(servidor: str, metrica: str, valor: float, threshold: float) -> dict:
#     """Registra e dispara um alerta quando uma métrica ultrapassa o limite."""
#     # TODO: adicione ao ALERTAS_DISPARADOS com timestamp
#     # Retorne {"alerta": "CRÍTICO", "servidor": ..., "metrica": ...,
#     #          "valor": ..., "threshold": ..., "timestamp": ...}
#     pass
#
# def listar_alertas(servidor: str = None) -> list:
#     """Lista alertas disparados, opcionalmente filtrados por servidor."""
#     # TODO: filtre ALERTAS_DISPARADOS por servidor se informado
#     pass
#
# # TESTES ESPERADOS:
# # coletar_metricas_servidor("web-01") → {"cpu_percent": 73, "memoria_percent": 45, ...}
# # disparar_alerta("web-01", "cpu_percent", 91, 80) → {"alerta": "CRÍTICO", ...}
# # listar_alertas("web-01") → [{"alerta": "CRÍTICO", ...}]
#
# # PROMPT DE TESTE PARA O AGENTE:
# # "Monitore os servidores web-01, web-02 e db-01.
# #  Dispare alertas para CPU > 80%, memória > 85% ou disco > 90%.
# #  Me dê um relatório final."


# =============================================================================
# EXERCÍCIO 9 — Agente com Contexto de Conversa (Multi-turn)
# =============================================================================
"""
CONCEITO: Manter histórico de conversa para que o agente lembre o contexto
de interações anteriores. Fundamental para assistentes reais.

SKILLS: conversation_history, multi_turn, context_management
"""

# from google import genai
# from google.genai import types
# import httpx, re, time
# from google.genai import errors as genai_errors
#
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
# client = genai.Client(api_key=GOOGLE_API_KEY, http_options={"verify_ssl": False})
#
# historico = []  # Lista de types.Content acumulados entre turnos
#
# def chat_com_memoria(mensagem_usuario: str, tools: list = None) -> str:
#     """Envia mensagem mantendo histórico completo da conversa."""
#     # TODO 1: adicione a mensagem ao historico como Content(role="user")
#     # TODO 2: chame client.models.generate_content com o historico inteiro como contents
#     # TODO 3: adicione a resposta ao historico como Content(role="model")
#     # TODO 4: retorne response.candidates[0].content.parts[0].text
#     pass
#
# # TESTES ESPERADOS (conversa multi-turn):
# # chat_com_memoria("Meu nome é Philippe e trabalho com Python.")
# # → "Olá Philippe! ..."
# # chat_com_memoria("Qual é o meu nome?")
# # → "Seu nome é Philippe." (o modelo lembrou!)
# # chat_com_memoria("E com o que eu trabalho?")
# # → "Você trabalha com Python." (contexto preservado)
#
# # PROMPT DE TESTE:
# # Rode as 3 perguntas em sequência e veja o agente manter contexto.


# =============================================================================
# EXERCÍCIO 10 — Agente Autônomo Completo: Assistente de Código
# =============================================================================
"""
CONCEITO: Agente completo com múltiplas tools que auxilia em tarefas de
desenvolvimento de software. Integra busca web, execução de código e análise.

SKILLS: code_assistant, autonomous_agent, tool_orchestration, full_pipeline

Este é o exercício mais avançado — combine tudo que aprendeu nos anteriores.
"""

# import subprocess, tempfile, os
# import requests, urllib3
# urllib3.disable_warnings()
#
# def executar_python(codigo: str) -> dict:
#     """Executa um trecho de código Python e retorna stdout/stderr."""
#     # TODO: use tempfile.NamedTemporaryFile para salvar o código
#     # Execute com subprocess.run(["python", arquivo], capture_output=True, timeout=10)
#     # Retorne {"stdout": ..., "stderr": ..., "returncode": ...}
#     # ATENÇÃO: em produção, use sandbox. Aqui é apenas para fins didáticos.
#     pass
#
# def buscar_documentacao(biblioteca: str, funcao: str = "") -> dict:
#     """Busca documentação de uma biblioteca Python via PyPI + docs."""
#     # TODO: GET https://pypi.org/pypi/{biblioteca}/json (verify=False)
#     # Extraia: versao, descricao, url_homepage
#     # Retorne {"biblioteca": ..., "versao": ..., "descricao": ..., "url": ...}
#     pass
#
# def analisar_erro(traceback: str) -> dict:
#     """Analisa um traceback Python e retorna tipo e linha do erro."""
#     # TODO: use re.search para extrair:
#     # - tipo do erro (ex: "ValueError", "TypeError")
#     # - mensagem do erro (última linha)
#     # - arquivo e linha (do último "File ...")
#     # Retorne {"tipo_erro": ..., "mensagem": ..., "arquivo": ..., "linha": ...}
#     pass
#
# def listar_pacotes_instalados() -> list:
#     """Lista pacotes Python instalados no ambiente atual."""
#     # TODO: subprocess.run(["pip", "list", "--format=json"], capture_output=True)
#     # Retorne lista de {"nome": ..., "versao": ...}
#     pass
#
# # TESTES ESPERADOS:
# # executar_python("print(2 + 2)")          → {"stdout": "4\n", "stderr": "", "returncode": 0}
# # executar_python("x = 1/0")               → {"stderr": "ZeroDivisionError...", "returncode": 1}
# # buscar_documentacao("requests")          → {"versao": "2.x.x", "descricao": "..."}
# # analisar_erro("...ValueError: invalid literal...")
# #   → {"tipo_erro": "ValueError", "mensagem": "invalid literal..."}
#
# # PROMPT DE TESTE PARA O AGENTE:
# # "Escreva e execute um código Python que calcula os 10 primeiros números de Fibonacci.
# #  Se der erro, analise e corrija automaticamente."
#
# # DESAFIO EXTRA:
# # Combine este agente com o ex09 (multi-turn) para criar um assistente
# # de código interativo com memória de sessão.


# =============================================================================
# GUIA DE PROGRESSÃO
# =============================================================================
"""
ORDEM SUGERIDA DE IMPLEMENTAÇÃO:

  Iniciante    → Ex01 (notas), Ex02 (confirmação), Ex04 (calculadora)
  Intermediário → Ex03 (busca web), Ex05 (retry/fallback), Ex06 (CSV)
  Avançado     → Ex07 (planner), Ex08 (monitoramento), Ex09 (multi-turn)
  Expert       → Ex10 (agente completo)

CONCEITOS ACUMULADOS POR EXERCÍCIO:

  Ex01 → tool com estado (dict global como "banco de dados")
  Ex02 → segurança e aprovação humana antes de ações destrutivas
  Ex03 → tool que acessa dados externos (web scraping / busca)
  Ex04 → múltiplas tools matemáticas encadeadas, output estruturado
  Ex05 → resiliência: retry automático + provider de fallback
  Ex06 → tools de dados: CSV, agregações, estatísticas
  Ex07 → agente multi-etapas com planejamento explícito
  Ex08 → agente autônomo com lógica de decisão (thresholds)
  Ex09 → conversação multi-turn com memória de contexto
  Ex10 → agente completo: execução de código + análise + docs + memória

DICA: Comece implementando e testando as funções Python diretamente
(sem o LLM). Só depois conecte ao agente. Isso facilita muito o debug.
"""

print("📋 Arquivo de exercícios futuros carregado.")
print("   Descomente o bloco do exercício que deseja implementar e bom código! 🚀")
