import sys
from langchain.tools import tool, BaseTool
from my_agent.models.request import QueryParams
from my_agent.config.database import run_db

sys.path.append("..")

@tool("aggregate_metric", description="Agrega uma métrica usando uma operação "
"(AVG, SUM, MIN, MAX, COUNT) e opcionalmente agrupa por uma coluna.")
def aggregate_metric(params: QueryParams):
    """
    Allowed operations: AVG, SUM, MIN, MAX, COUNT
    """
    if params.group_by:
        query = f"""
            SELECT {params.group_by}, {params.operation}({params.column})
            FROM customers
            GROUP BY {params.group_by}
        """
    else:
        query = f"""
            SELECT {params.operation}({params.column})
            FROM customers
        """
    resultado = run_db(query)
    return str(resultado)

@tool("filter_data", description="Filtra dados com base em " \
"critérios especificados.")
def filter_data(params: QueryParams):
    """
    Allowed operators: >, <, =, >=, <=
    """
    query = f"""
    SELECT *
    FROM customers
    WHERE {params.column} {params.operator} {params.value}
    LIMIT {params.limit}
    """
    resultado = run_db(query)
    return str(resultado)

@tool("top_students", description="Retorna os melhores estudantes " \
"com base em uma métrica.")
def top_students(params: QueryParams):
    query = f"""
    SELECT *
    FROM customers
    ORDER BY {params.column} DESC
    LIMIT {params.limit}
    """
    resultado = run_db(query)
    return str(resultado)

@tool("get_table_schema", description="Retorna o schema (estrutura) da tabela " \
"customers com informações sobre cada coluna e seu tipo de dado.")
def get_table_schema(params: QueryParams):
    """
    Returns the schema of the customers table with column names, types, and descriptions
    """
    schema_info = """
    SCHEMA DA TABELA 'customers':
    
    📊 DADOS DEMOGRÁFICOS:
    - student_id (INT): Identificador único do estudante
    - age (INT): Idade do estudante
    - gender (TEXT): Gênero (Male/Female)
    - academic_level (TEXT): Nível acadêmico (High School/Undergraduate/Graduate)
    
    📚 HÁBITOS DE ESTUDO:
    - study_hours (FLOAT): Horas de estudo por semana
    - self_study_hours (FLOAT): Horas de auto-estudo por semana
    - online_classes_hours (FLOAT): Horas em aulas online por semana
    
    📱 COMPORTAMENTO DIGITAL:
    - social_media_hours (FLOAT): Horas em redes sociais por semana
    - gaming_hours (FLOAT): Horas de jogos por semana
    - screen_time_hours (FLOAT): Tempo total de tela por semana
    
    🏃 SAÚDE E ESTILO DE VIDA:
    - sleep_hours (FLOAT): Horas de sono por noite
    - exercise_minutes (INT): Minutos de exercício por semana
    - caffeine_intake_mg (INT): Ingestão de cafeína em mg por dia
    - mental_health_score (INT): Score de saúde mental (0-100)
    
    ⚖️ PRESSÃO PROFISSIONAL E ACADÊMICA:
    - part_time_job (INT): 1 se tem trabalho part-time, 0 caso contrário
    - upcoming_deadline (INT): 1 se há prazo próximo, 0 caso contrário
    - internet_quality (TEXT): Qualidade da internet (Poor/Average/Good/Excellent)
    
    📈 VARIÁVEIS ALVO (Predição):
    - focus_index (FLOAT): Índice de foco (0-100)
    - burnout_level (FLOAT): Nível de burnout (0-100)
    - productivity_score (FLOAT): Score de produtividade (0-100)
    - exam_score (FLOAT): Pontuação no exame (0-100)
    
    TOTAL: 21 colunas, 5000 registros de estudantes
    """
    return schema_info

CUSTOM_TOOLS: list[BaseTool] = [
    aggregate_metric,
    filter_data,
    top_students,
    get_table_schema,
]