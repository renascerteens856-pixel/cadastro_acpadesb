from flask import Flask
from flask_cors import CORS
from blueprints.adolescentes import adolescentes_bp  # importa o blueprint

app = Flask(__name__)

# Libera acesso do front-end ao backend
CORS(app)

# Registra o Blueprint na rota /adolescentes
app.register_blueprint(adolescentes_bp, url_prefix="/adolescentes")


@app.get("/")
def home():
    return {"status": "Servidor rodando!", "versao": "1.0"}


if __name__ == "__main__":
    app.run(debug=True)
