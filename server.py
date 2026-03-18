from flask import Flask, send_from_directory
from flask_cors import CORS
from blueprints.adolescentes import adolescentes_bp
from blueprints.congregacoes import congregacoes_bp
from blueprints.criancas import criancas_bp
import os

app = Flask(__name__, static_folder="static")
CORS(app)

# Blueprint
app.register_blueprint(adolescentes_bp, url_prefix="/adolescentes")
app.register_blueprint(congregacoes_bp, url_prefix="/congregacoes")
app.register_blueprint(criancas_bp, url_prefix="/criancas")

# Rota principal
@app.route('/')
def home():
    return send_from_directory('static', 'index.html')

# Rota para arquivos estáticos
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

# Rota de teste para verificar se a API está funcionando
@app.route('/ping')
def ping():
    return jsonify({"status": "ok", "mensagem": "API funcionando!"})

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
