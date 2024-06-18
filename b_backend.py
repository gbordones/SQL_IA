import sqlite3
import os
from openai import OpenAI
import a_env_vars
import re

# Configurar la API de OpenAI

client = OpenAI(api_key=a_env_vars.OPENAI_API_KEY)

# 1. Cargar la base de datos con sqlite3
db_path = "ecommerce.db"
conn = sqlite3.connect(db_path, check_same_thread=False)
cursor = conn.cursor()

 #2. Función para crear la consulta en lenguaje natural

def create_query_us(input_usuario):
    formato = """
    Dada una pregunta del usuario:
    1. Crea una consulta de sqlite3.
    2. Revisa los resultados.
    3. Devuelve el dato.
    4. Si tienes que hacer alguna aclaración o devolver cualquier texto, que sea siempre en español.
    Pregunta del usuario: "{question}"
  """
    return formato.format(question=input_usuario)

def create_query(input_usuario):
    formato = """
    Dada una pregunta del usuario:
    1. Crea solo una consulta de sqlite3.
    2. La consulta debe ser una sola línea de código SQL sin ninguna explicación adicional.
    Pregunta del usuario: "{question}"
    """
    return formato.format(question=input_usuario)

# 3. Función para interactuar con OpenAI GPT-3.5 usando la nueva API
def ask_openai(prompt):
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Eres un asistente útil."},# que genera consultas SQL"},
        {"role": "user", "content": prompt}
    ])
    return response.choices[0].message.content.strip()

def extract_sql_query(response):
    match = re.search(r"SELECT.*?;", response, re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(0)
    else:
        raise ValueError("No se encontró una consulta SQL válida en la respuesta.")


# 4. Función para hacer la consulta Usuario
def consulta_us(input_usuario):
    prompt_us = create_query_us(input_usuario)
    query_us = ask_openai(prompt_us)

    try:
   
        #cursor.execute(query)
        print(query_us)
        results = query_us

        
        return results
   
    except Exception as e:
   
        return f"Error al ejecutar la consulta: {str(e)}"
        
def consulta(input_usuario):
    prompt = create_query(input_usuario)
    query = ask_openai(prompt)

    try:
   
        cursor.execute(query)
        results = cursor.fetchall()
        
        return results
   
    except Exception as e:
   
        return f"Error al ejecutar la consulta: {str(e)}"

# 5. Cerrar la conexión cuando ya no sea necesaria


def close_connection():
    conn.close()
