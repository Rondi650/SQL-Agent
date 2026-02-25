# 🤖 SQL Agent - Frontend Streamlit

Frontend simples em Streamlit para interagir com o SQL Agent via API REST.

## 🚀 Como Usar

### 1. **Instalar Dependências**

```bash
pip install -r requirements_frontend.txt
```

### 2. **Iniciar a API**

Em um terminal, execute a API do agente:

```bash
uvicorn main:app --reload
```

A API estará disponível em `http://localhost:8000`

### 3. **Iniciar o Streamlit Frontend**

Em outro terminal, execute:

```bash
streamlit run streamlit_app.py
```

O frontend abrirá automaticamente em `http://localhost:8501`

---

## 📋 Recursos

✅ **Chat em tempo real** - Converse com o agente SQL
✅ **Histórico de mensagens** - Todas as mensagens são mantidas na sessão
✅ **Exemplos rápidos** - Botões com perguntas pré-formatadas
✅ **Metadados** - Veja timestamp e thread ID de cada resposta
✅ **Configurável** - Mude a URL da API na barra lateral
✅ **Links úteis** - Acesso direto à documentação Swagger/ReDoc

---

## 🎯 Exemplos de Perguntas

Você pode fazer perguntas como:

- "Qual é o NPS geral?"
- "Qual o NPS de Diane em janeiro de 2025?"
- "Qual agente atendeu mais chamadas?"
- "Qual é o tempo médio de atendimento?"
- "Quantas chamadas foram atendidas em janeiro?"

---

## 🔧 Configuração

Na **barra lateral**, você pode:

1. **Alterar URL da API** - Se a API está em outro host/porta
2. **Ver Thread ID** - Identificador da conversa atual
3. **Exemplos de Perguntas** - Clique para inserir automática
4. **Links Úteis** - Acesso à documentação da API

---

## 📊 Estrutura das Respostas

Cada resposta mostra:

- **Mensagem do agente** - Resposta formatada
- **Data/Hora** - Quando a resposta foi gerada
- **Thread ID** - Identificador da conversa

---

## 🐛 Troubleshooting

### Erro: "Não foi possível conectar à API"
- Verifique se a API está rodando: `http://localhost:8000/docs`
- Verifique a URL configurada na barra lateral
- Reinicie a API: `uvicorn main:app --reload`

### Erro: "Requisição expirou"
- Consultas muito complexas podem tomar mais tempo
- Tente uma pergunta mais simples
- Aumente o timeout se necessário

### Chat não carrega histórico
- A sessão é mantida apenas durante a execução
- Recarregue a página para resetar (há botão "Limpar Chat")

---

## 📦 Dependências

- **streamlit** - Framework para criar a interface web
- **requests** - Cliente HTTP para chamar a API

---

## 🔗 Links Úteis

- **Documentação Streamlit**: https://docs.streamlit.io
- **API Docs**: http://localhost:8000/docs (quando a API estiver rodando)
- **Projeto Principal**: ../README.md

---

## 💡 Dicas

1. Mantenha a API rodando enquanto usa o frontend
2. Use botões de exemplos para testar funcionalidades
3. Veja os detalhes de cada resposta para entender como o agente resolveu
4. A conversa é mantida apenas na sessão - recarregue para limpar
