import openai
import os
import time 
import json

openai.api_key = os.getenv("OPENAI_API_KEY")
ASSISTANT_ID = os.getenv("OPENAI_API_ASSISTENT_KEY")

# Substitua pela sua chave da API da OpenAI

def classificar_transacao(mensagem: str) -> dict:
    # Cria um novo thread
    thread = openai.beta.threads.create()

    # Adiciona a mensagem do usuário ao thread
    openai.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=mensagem
    )

    # Executa o assistente com base no thread
    run = openai.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=ASSISTANT_ID
    )

    # Aguarda até o processamento terminar
    while True:
        run_status = openai.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        if run_status.status == "completed":
            break
        elif run_status.status == "failed":
            raise RuntimeError("Falha ao processar com o assistente.")
        time.sleep(1)

    # Obtém a última resposta do assistente
    messages = openai.beta.threads.messages.list(thread_id=thread.id)
    resposta_texto = messages.data[0].content[0].text.value.strip()

    # Tenta converter a resposta em JSON (se possível)
    try:
        resposta_json = json.loads(resposta_texto)
        return resposta_json
    except json.JSONDecodeError:
        return {"erro": "Não foi possível converter para JSON", "texto": resposta_texto}


