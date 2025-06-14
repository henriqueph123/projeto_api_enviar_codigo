from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Carrega variáveis do arquivo .env

app = Flask(__name__)
CORS(app)

BREVO_API_KEY = os.getenv("BREVO_API_KEY")

if not BREVO_API_KEY:
    raise RuntimeError("A variável de ambiente BREVO_API_KEY não está definida!")

@app.route("/api/enviar_codigo", methods=["POST"])
def enviar_codigo():
    data = request.json
    email_ou_telefone = data.get("contato")
    if not email_ou_telefone:
        return jsonify({"error": "Contato (email ou telefone) obrigatório."}), 400

    codigo = str(random.randint(100000, 999999))
    templates = ["template1.html", "template2.html", "template3.html"]
    template_escolhido = random.choice(templates)

    try:
        template_path = os.path.join(os.path.dirname(__file__), 'templates', template_escolhido)
        with open(template_path, "r", encoding="utf-8") as f:
            html_template = f.read()
    except Exception as e:
        return jsonify({"error": f"Erro ao carregar template: {str(e)}"}), 500

    html_com_codigo = html_template.replace("{{codigo}}", codigo)

    body = {
        "sender": {"name": "Mercado Livre", "email": "suellepromotora@gmail.com"},
        "to": [{"email": email_ou_telefone, "name": email_ou_telefone}],
        "subject": "Código de Verificação",
        "htmlContent": html_com_codigo
    }

    headers = {
        "Content-Type": "application/json",
        "api-key": BREVO_API_KEY
    }

    response = requests.post("https://api.brevo.com/v3/smtp/email", json=body, headers=headers)

    if response.status_code != 201:
        return jsonify({"error": f"Falha ao enviar e-mail: {response.text}"}), 500

    return jsonify({"message": "Email enviado com sucesso!", "codigo": codigo})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
