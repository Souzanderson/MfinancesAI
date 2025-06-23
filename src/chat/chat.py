import openai
import os
import time 
import json

openai.api_key = os.getenv("OPENAI_API_KEY")
ASSISTANT_ID = os.getenv("OPENAI_API_ASSISTENT_KEY")

class ContextUser:
    context = {}

    def append(self, message: dict, user: str):
        ContextUser.context[user] = ContextUser.context.get(user, [])
        ContextUser.context[user].append(message)
        if len(ContextUser.context[user]) > 20:
            ContextUser.context[user] = ContextUser.context[user][-20:]

    def get_context(self, user: str) -> str:
        if user in ContextUser.context:
            return "últimas mensagens: " + "\n".join(ContextUser.context[user])
        return f""
# Substitua pela sua chave da API da OpenAI

def classificar_transacao(message_received: str, user:str) -> dict:
    # Cria um novo thread
    thread = openai.beta.threads.create()
    context = ContextUser()
    message_context = context.get_context(user)
    print(f"Contexto para o usuário {user}: {message_context}")
    # Adiciona a mensagem do usuário ao thread
    openai.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=f"{message_context}\n\n{message_received}",
        metadata={"user": user, "context": message_context}
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
    context.append(f"Pedido: {message_received}", user)
    context.append(f"Resposta: {resposta_texto}", user)
    # Tenta converter a resposta em JSON (se possível)
    try:
        resposta_json = json.loads(resposta_texto)
        return resposta_json
    except json.JSONDecodeError:
        return {"erro": "Não foi possível converter para JSON", "texto": resposta_texto}


