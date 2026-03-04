# SQL Agent - Agente Inteligente de Análise de Dados

Um agente inteligente baseado em IA (GPT + LangGraph) que transforma perguntas em linguagem natural em consultas SQL e análises de dados.

## Descrição

O SQL Agent converte perguntas em português para consultas SQL ou ferramentas customizadas de análise, eliminando a necessidade de conhecimento técnico de SQL. Inclui dataset completo para testes imediatos sem configuração de banco de dados externo.

**Características principais:**
- Compreensão de perguntas em linguagem natural
- Roteamento automático para ferramentas apropriadas
- Validação de consultas SQL antes da execução
- Histórico persistente de conversas
- Interface web moderna com Streamlit
- Dataset pré-carregado para testes

## Pré-requisitos

- Python 3.10 ou superior
- Chave de API OpenAI
- (Opcional) SQL Server para produção

**Nota:** O projeto inclui um dataset SQLite pré-configurado para testes, não requer setup de banco de dados.

## Instalação

### 1. Clone o repositório
```bash
cd PROJETO-4---SQL_AGENT
```

### 2. Configure o ambiente virtual
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure a chave OpenAI
```bash
export OPENAI_API_KEY="sua-chave-aqui"  # Linux/Mac
# ou
set OPENAI_API_KEY=sua-chave-aqui  # Windows
```

## Execução

### Terminal 1 - API
```bash
python main.py
```
Disponível em `http://localhost:8000`

### Terminal 2 - Interface Web
```bash
streamlit run streamlit_app.py
```
Acesso em `http://localhost:8501`

O dataset pré-carregado contém dados de produtividade estudantil para testes imediatos.

## Recursos

- Chat em tempo real com respostas inteligentes baseadas em IA
- Exemplos de perguntas pré-formatadas por categoria
- Histórico de mensagens persistente durante a sessão
- Metadados (timestamp e ID de thread para cada resposta)
- Avatares customizados para usuário e assistente
- Documentação interativa (Swagger/ReDoc)
- Dataset incluído para testes imediatos

## Exemplos de Consultas

```
"Qual é a nota média de exame dos estudantes?"
"Quais são os 10 melhores estudantes por nota?"
"Qual é a média de horas de estudo?"
"Qual é o score médio de saúde mental?"
"Qual a nota média por nível acadêmico?"
```

## Estrutura do Projeto

```
PROJETO-4---SQL_AGENT/
├── main.py                    # Servidor API FastAPI
├── streamlit_app.py           # Interface web Streamlit
├── requirements.txt           # Dependências do projeto
│
├── my_agent/
│   ├── agent.py              # Orquestração do agente
│   ├── config/               
│   │   ├── database.py       # Configuração de conexão
│   │   ├── settings.py       # Configurações LLM
│   │   ├── prompts.py        # Instruções de sistema
│   │   └── db.sqlite3        # Dataset para testes
│   ├── models/               
│   │   ├── request.py        # Modelos de entrada
│   │   └── response.py       # Modelos de saída
│   └── utils/                
│       ├── tools.py          # Ferramentas disponíveis
│       ├── nodes.py          # Nós do workflow
│       ├── helpers.py        # Funções auxiliares
│       └── images/           # Avatares do chat
```

## Configuração

A barra lateral da aplicação permite:
- Modificar URL da API remotamente
- Visualizar ID da conversa atual
- Acessar exemplos de perguntas por categoria
- Consultar documentação da API (Swagger/ReDoc)

## Troubleshooting

| Problema | Solução |
|----------|---------|
| Erro ao conectar na API | Verifique se `main.py` está rodando em `http://localhost:8000` |
| Requisição expirada | Simplifique a pergunta; consultas complexas demoram mais tempo |
| Avatares não aparecem | Confirme que as imagens estão em `my_agent/utils/images/` |
| Chat vazio após refresh | Use o botão "Limpar Chat" para resetar a sessão |
| Erro de chave OpenAI | Configure `OPENAI_API_KEY` nas variáveis de ambiente |

## Documentação da API

Após iniciar o servidor, acesse:
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

## Desenvolvimento

Para adicionar novas ferramentas:
1. Defina a ferramenta em `my_agent/utils/tools.py`
2. Registre no agente em `my_agent/agent.py`
3. Atualize os prompts em `my_agent/config/prompts.py`

## Licença

Projeto educacional para análise de dados inteligente.
