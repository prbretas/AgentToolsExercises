"""
🗓️ Seção 2 — Calendar Mock
Testa list_events e create_event diretamente, sem chamar nenhuma API.
"""

from datetime import datetime, date

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


# ── Testes ────────────────────────────────────────────────────────────────────
hoje_inicio = f"{hoje}T00:00:00-03:00"
hoje_fim    = f"{hoje}T23:59:59-03:00"

print("📅 Eventos hoje (antes de criar):")
for e in list_events(hoje_inicio, hoje_fim):
    print(f"  - {e['titulo']}  {e['inicio']} → {e['fim']}")

print("\n➕ Criando evento 'Sprint Review' às 14h...")
resultado = create_event("Sprint Review", f"{hoje}T14:00:00-03:00", f"{hoje}T15:00:00-03:00")
print("  Resultado:", resultado)

print("\n📅 Eventos hoje (depois de criar):")
for e in list_events(hoje_inicio, hoje_fim):
    print(f"  - {e['titulo']}  {e['inicio']} → {e['fim']}")

print("\n✅ Seção 2 OK!")
