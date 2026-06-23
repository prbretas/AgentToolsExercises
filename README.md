# 🤖 Aula — Tool-Use: Function Calling Nativo com Python

**IA para DEVs · LAB 365 / aSCTI.SC · Módulo 2 · Semana 03**

Este projeto explora como modelos de linguagem (LLMs) podem chamar funções Python reais — o mecanismo chamado **Function Calling** ou **Tool Use**. Em vez de apenas gerar texto, o modelo decide quando e como usar ferramentas externas para responder a uma pergunta.

---

## 📂 Estrutura do Projeto

```
Aula-2206/
├── README.md                          ← este arquivo
├── APIkeys.md                         ← suas chaves de API (não compartilhe)
├── exerciciospython220626.md          ← enunciado original do exercício
├── exercicio_220626.py                ← versão monolítica (referência)
└── exercicios/
    ├── ex02_calendar_mock.py          ← agenda em memória (sem API)
    ├── ex03_automatic_function_calling.py  ← agente Gemini com tools
    ├── ex04_manual_tool_call.py       ← inspecionar tool call bruto
    ├── ex05_groq.py                   ← Groq / Llama via SDK OpenAI
    ├── ex06_sequential_calling.py     ← encadeamento de tools (clima)
    └── ex07_tool_robusta.py           ← validação e tratamento de erros
```

---
## Link do exercicio
https://colab.research.google.com/drive/1NSx7eF4gmX4Z45ImBTRjuPC2QG0n7tDP#scrollTo=4Hk9Fah24RPL


## ⚙️ Instalação

```bash
pip install google-genai openai requests httpx certifi urllib3
```

---

## 📚 Conceitos Abordados

### O que é Tool Use / Function Calling?

Um LLM normalmente só gera texto. Com **Function Calling**, o modelo pode identificar que precisa de uma informação externa (ex: clima, agenda, banco de dados) e emitir uma chamada estruturada para uma função Python — com nome e argumentos. Você executa a função e devolve o resultado ao modelo, que então formula a resposta final.

O fluxo básico é:

```
Usuário → Prompt → Modelo → [decide chamar tool] → Função Python
                                                          ↓
Usuário ← Resposta final ← Modelo ← Resultado da função
```

---

## 🗂️ Exercícios

### `ex02_calendar_mock.py` — Agenda em Memória

**Conceito:** como criar **tools** que o modelo pode chamar.

Uma tool é simplesmente uma função Python com:
- **Nome** descritivo
- **Docstring** clara (o modelo lê isso para entender o que a função faz)
- **Type hints** nos parâmetros (o modelo usa para montar os argumentos certos)

```python
def list_events(data_inicio: str, data_fim: str) -> list:
    """Lista eventos do calendário entre duas datas (ISO 8601)."""
    ...
```

Este exercício não chama nenhuma API de IA — testa as funções diretamente, confirmando que a lógica de filtragem e criação de eventos está correta.

**Como rodar:** `python exercicios/ex02_calendar_mock.py`

---

### `ex03_automatic_function_calling.py` — Agente com Gemini

**Conceito:** **Automatic Function Calling** — o modelo executa o loop inteiro sozinho.

Aqui o Gemini recebe as funções como tools e decide automaticamente quando chamar cada uma. O exercício implementa o loop manualmente para deixar explícito o que acontece nos bastidores:

1. Modelo recebe o prompt
2. Modelo emite um `function_call` (nome + args)
3. Você executa a função Python
4. Você devolve o resultado como `function_response`
5. Modelo gera a resposta final em texto

**Duas perguntas testadas:**
- "O que tenho hoje na agenda?" → chama `list_events`
- "Agende Sprint Review se houver slot livre entre 14h e 18h" → chama `list_events` e depois `create_event`

**Como rodar:** `python exercicios/ex03_automatic_function_calling.py`

---

### `ex04_manual_tool_call.py` — Inspecionando o Tool Call

**Conceito:** **modo manual** com `FunctionCallingConfig(mode="ANY")`.

Força o modelo a **sempre** emitir um tool call (sem executar), permitindo inspecionar exatamente o que ele gera antes de qualquer execução. Útil para:
- Depuração
- Validar que o modelo está chamando a função correta
- Entender o formato dos argumentos gerados

```
Tool : list_events
Args : {'data_inicio': '2026-06-22T00:00:00-03:00', 'data_fim': '2026-06-22T23:59:59-03:00'}
```

**Como rodar:** `python exercicios/ex04_manual_tool_call.py`

---

### `ex05_groq.py` — Portabilidade: Groq com SDK OpenAI

**Conceito:** **qualquer provedor OpenAI-compatible** funciona com o mesmo código.

O SDK `openai` aceita um `base_url` customizado. Trocando apenas `api_key` e `base_url`, o mesmo código roda em:
- OpenAI (GPT-4o, etc.)
- Groq (Llama 3.3 70B) ← este exercício
- Azure OpenAI
- Qualquer outro provedor compatível

O exercício mostra que o modelo Llama, rodando no Groq, também emite um `tool_calls` estruturado quando perguntado sobre a agenda — mesmo sem "entender" a agenda, o modelo entende que precisa consultar uma tool para responder.

**Como rodar:** `python exercicios/ex05_groq.py`

---

### `ex06_sequential_calling.py` — Encadeamento de Tools

**Conceito:** **Sequential Function Calling** — o output de uma tool vira o input da próxima.

O Gemini encadeia automaticamente:

```
"Qual a temperatura em Florianópolis?"
    ↓
get_city_coordinates("Florianópolis")  →  {lat: -27.59, lon: -48.54}
    ↓
get_weather(-27.59, -48.54)            →  {temperatura: 16°C, vento: 18km/h}
    ↓
"A temperatura atual em Florianópolis é de 16°C..."
```

O modelo decide sozinho que precisa das coordenadas antes do clima — sem nenhum código de orquestração extra. Isso é o que torna agents poderosos: o raciocínio sobre qual ferramenta usar e em que ordem é do próprio modelo.

**APIs usadas (gratuitas, sem autenticação):**
- [Nominatim / OpenStreetMap](https://nominatim.openstreetmap.org) — geocoding
- [Open-Meteo](https://open-meteo.com) — clima

**Como rodar:** `python exercicios/ex06_sequential_calling.py`

---

### `ex07_tool_robusta.py` — Tool com Tratamento de Erros

**Conceito:** **tools nunca devem quebrar o loop do agente**.

Regra de ouro: uma tool deve **sempre retornar um `dict`**, inclusive em caso de erro. Se a função lançar uma exceção, o agente trava. Se retornar um dict com `{"error": "..."}`, o modelo pode ler o erro e tomar uma decisão inteligente (tentar novamente, informar o usuário, usar um fallback).

Três camadas de proteção implementadas:
1. **Validação de input** — antes de qualquer chamada de rede
2. **Timeout explícito** — evita que o agente fique pendurado
3. **Try/except por tipo** — respostas diferentes para cada tipo de erro

```python
# ✅ correto — o agente continua funcionando
except requests.Timeout:
    return {"error": "Timeout ao consultar a API de clima (>5s)"}

# ❌ errado — quebra o loop do agente
except requests.Timeout:
    raise
```

**Como rodar:** `python exercicios/ex07_tool_robusta.py`

---

## 🔑 APIs e Modelos Utilizados

| Serviço | Modelo | Uso |
|---------|--------|-----|
| Google Gemini | `gemini-2.0-flash-lite` | Automatic function calling, inspeção, clima |
| Groq | `llama-3.3-70b-versatile` | Portabilidade via SDK OpenAI |
| Open-Meteo | — | Dados de clima (gratuito, sem auth) |
| Nominatim | — | Geocoding (gratuito, sem auth) |

---

## ⚠️ Observações

- **Rate limit:** a chave gratuita do Gemini tem limite de ~5 req/min. Os exercícios incluem retry automático com espera inteligente.
- **SSL corporativo:** em redes com proxy self-signed, os arquivos já incluem `verify=False` nas chamadas HTTP. Isso é normal em ambientes empresariais.
- **`!pip` não funciona no terminal:** essa sintaxe é exclusiva do Jupyter/Colab. No terminal Windows use `pip install ...` normalmente.
