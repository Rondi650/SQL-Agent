# AGENTS.md

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY="sk-..."
```

## Run

Two terminals (or use Docker):

```bash
# Terminal 1 — API (FastAPI on :8081)
uvicorn main:app --reload --port 8081

# Terminal 2 — UI (Streamlit on :8501)
streamlit run streamlit_app.py
```

Docker: `docker compose up` (runs both via `scripts/entrypoint.sh`).

## Services

- `main.py` — FastAPI server with two endpoints: `POST /chat` and `POST /chat/resume`
- `streamlit_app.py` — Streamlit frontend calls API at `http://localhost:8081/chat`; shows approval UI when `status: "awaiting_approval"`
- Agent defined in `my_agent/agent.py` (LangGraph StateGraph, InMemorySaver)
- API docs at `/docs` (Swagger) and `/redoc`

## Architecture

- **Model**: `gpt-5.1-2025-11-13`, temperature=0 (`my_agent/config/settings.py`)
- **Tools-only**: LLM must use one of 4 custom tools — NO direct SQL generation
- **Tools**: `get_table_schema`, `aggregate_metric`, `filter_data`, `top_students`
- **Graph**: `START → roteador → (human_approval → tools → roteador) or __end__`
- **Recursion limit**: 10 (in `THREAD_CONFIG`)

## Human-in-the-Loop

The agent implements human approval via LangGraph `interrupt()` and `Command`:

- After `roteador` proposes tool calls, the graph pauses at `human_approval`
- The API returns `{"status": "awaiting_approval", "interrupt": {...}}`
- Client calls `POST /chat/resume` with `{"thread_id", "action": "approve|reject", "feedback"}`
- **Approve**: proceeds to `tools` node for execution
- **Reject**: routes back to `roteador` with feedback; the node strips orphaned `tool_calls` from the last `AIMessage` (same-ID replacement via `add_messages` reducer) so OpenAI does not receive invalid message sequences
- A message sanitizer in `roteador` (`_sanitize_messages`) strips any remaining orphaned tool_calls before each LLM call as a safety net

## API Endpoints

- `POST /chat` — Start a conversation. Returns `RespostaModel` or `{"status": "awaiting_approval", ...}`
- `POST /chat/resume` — Resume after an interrupt with human decision (`ResumeModel`)

## Database

- SQLite at `my_agent/config/db.sqlite3` — auto-created from CSV on import
- Table `customers`, 21 columns, 5000 rows (student productivity dataset)
- Production: set `DATABASE_URL=mssql+pyodbc://...` in `.env`

## Gotchas

- `python-dotenv` is imported in `settings.py` but **missing from `requirements.txt`** — install manually if `ImportError`
- `streamlit_app.py:221` error message says port 8000 but API runs on **8081**
- `database.py` has **import side effects**: loads CSV, creates/replaces SQLite DB on every import
- `agent.py` generates `agent_workflow.png` on import (side effect)
- No tests, no CI, no linting/typecheck config
- Question length capped at 200 chars (`PerguntaModel.pergunta`)
- Human-in-the-loop adds complexity: the `roteador` node includes `_sanitize_messages` to prevent OpenAI API errors from orphaned `tool_calls` when rejections occur
