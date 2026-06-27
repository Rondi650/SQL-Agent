# SQL Agent - Intelligent Data Analysis Agent

An intelligent AI-based agent (GPT + LangGraph) that transforms natural language questions into SQL queries and data analysis.

Note: Model used as a laboratory for learning and applying concepts.

## Description

SQL Agent converts Portuguese questions into SQL queries or custom analysis tools, eliminating the need for technical SQL knowledge. Includes a complete dataset for immediate testing without external database configuration.

**Key Features:**
- Natural language question comprehension
- Automatic routing to appropriate tools
- SQL query validation before execution
- Persistent conversation history
- Modern web interface with Streamlit
- Pre-loaded dataset for testing

## Prerequisites

- Python 3.10 or higher
- OpenAI API Key
- (Optional) SQL Server for production

**Note:** The project includes a pre-configured SQLite dataset for testing, no database setup required.

## Installation

### 1. Clone the repository
```bash
cd PROJETO-4---SQL_AGENT
```

### 2. Set up virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate  # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure OpenAI key
```bash
export OPENAI_API_KEY="your-key-here"  # Linux/Mac
# or
set OPENAI_API_KEY=your-key-here  # Windows
```

## Execution

### Terminal 1 - API
```bash
python main.py
```
Available at `http://localhost:8000`

### Terminal 2 - Web Interface
```bash
streamlit run streamlit_app.py
```
Access at `http://localhost:8501`

The pre-loaded dataset contains student productivity data for immediate testing.

## Features

- Real-time chat with intelligent AI-based responses
- Pre-formatted example questions by category
- Persistent message history during the session
- Metadata (timestamp and thread ID for each response)
- Custom avatars for user and assistant
- Interactive documentation (Swagger/ReDoc)
- Included dataset for immediate testing

## Query Examples

```
"What is the average exam score of students?"
"Who are the top 10 students by score?"
"What is the average study hours?"
"What is the average mental health score?"
"What is the average score by academic level?"
```

## Project Structure

```
PROJETO-4---SQL_AGENT/
├── main.py                    # FastAPI Server
├── streamlit_app.py           # Streamlit Web Interface
├── requirements.txt           # Project dependencies
│
├── my_agent/
│   ├── agent.py              # Agent orchestration
│   ├── config/               
│   │   ├── database.py       # Connection configuration
│   │   ├── settings.py       # LLM settings
│   │   ├── prompts.py        # System instructions
│   │   └── db.sqlite3        # Test dataset
│   ├── models/               
│   │   ├── request.py        # Input models
│   │   └── response.py       # Output models
│   └── utils/                
│       ├── tools.py          # Available tools
│       ├── nodes.py          # Workflow nodes
│       ├── helpers.py        # Helper functions
│       └── images/           # Chat avatars
```

## Configuration

The application sidebar allows:
- Modify remote API URL
- View current conversation ID
- Access example questions by category
- Consult API documentation (Swagger/ReDoc)

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Error connecting to API | Check if `main.py` is running at `http://localhost:8000` |
| Request timed out | Simplify the question; complex queries take more time |
| Avatars not showing | Confirm images are in `my_agent/utils/images/` |
| Empty chat after refresh | Use the "Clear Chat" button to reset the session |
| OpenAI key error | Configure `OPENAI_API_KEY` in environment variables |

## API Documentation

After starting the server, access:
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

## Development

To add new tools:
1. Define the tool in `my_agent/utils/tools.py`
2. Register in the agent at `my_agent/agent.py`
3. Update prompts in `my_agent/config/prompts.py`

## License

Educational project for intelligent data analysis.
