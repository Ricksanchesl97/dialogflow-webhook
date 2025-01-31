main.py
from flask import Flask, request, jsonify
import openai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permite conexões externas

# 🔑
OPENAI_API_KEY = "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"

@app.route('/')
def home():
    return "Webhook do ChatGPT rodando com sucesso!"

# Endpoint que receberá as mensagens do Dialogflow CX
@app.route('/webhook', methods=['POST'])
def webhook():
    body = request.get_json()

    # Captura a pergunta do usuário enviada pelo Dialogflow
    user_query = body.get("queryResult", {}).get("queryText", "Pergunta não reconhecida.")

    # Enviar a pergunta para o ChatGPT API
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": user_query}],
        api_key=OPENAI_API_KEY
    )

    # Captura a resposta do ChatGPT
    chatgpt_response = response["choices"][0]["message"]["content"]

    # Retorna a resposta para o Dialogflow
    return jsonify({
        "fulfillment_response": {
            "messages": [{"text": {"text": [chatgpt_response]}}]
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
