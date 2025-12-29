from flask import Blueprint, request, jsonify
from db_config import connect_db

# ======================================================
# CONFIG
# ======================================================
supabase = connect_db()
TABELA = "congregacoes"

congregacoes_bp = Blueprint(
    "congregacoes",
    __name__,
    url_prefix="/congregacoes"
)

# ======================================================
# LISTAR TODOS
# ======================================================
@congregacoes_bp.route("/", methods=["GET"])
def listar():
    try:
        response = (
            supabase
            .table(TABELA)
            .select("*")
            .order("id", desc=False)
            .execute()
        )

        dados = response.data or []

        resultado = []
        for item in dados:
            resultado.append({
                'nome': item.get('nome')
            })

        return jsonify(resultado), 200

    except Exception as e:
        return jsonify({
            "erro": "Erro ao listar adolescentes",
            "detalhes": str(e)
        }), 500


# ======================================================
# BUSCAR UM
# ======================================================
@congregacoes_bp.route("/<int:id>", methods=["GET"])
def buscar(id):
    try:
        response = (
            supabase
            .table(TABELA)
            .select("*")
            .eq("id", id)
            .single()
            .execute()
        )

        item = response.data

        if not item:
            return jsonify({"erro": "Adolescente não encontrado"}), 404

        return jsonify({
            'nome': item.get('nome')
        }), 200

    except Exception as e:
        return jsonify({
            "erro": "Erro ao buscar adolescente",
            "detalhes": str(e)
        }), 500


# ======================================================
# CADASTRAR
# ======================================================
@congregacoes_bp.route("/", methods=["POST"])
def cadastrar():
    try:
        data = request.get_json() or {}

        if not data.get("nome"):
            return jsonify({"erro": "Campo 'nome' é obrigatório"}), 400


        payload = {
            'nome':data.get('nome')
        }

        response = (
            supabase
            .table(TABELA)
            .insert(payload)
            .execute()
        )

        return jsonify(response.data[0]), 201

    except Exception as e:
        return jsonify({
            "erro": "Erro ao cadastrar adolescente",
            "detalhes": str(e)
        }), 500


# ======================================================
# ATUALIZAR
# ======================================================
@congregacoes_bp.route("/<int:id>", methods=["PUT"])
def atualizar(id):
    try:
        data = request.get_json() or {}

        payload = {
            'nome': data.get('nome')
        }

        response = (
            supabase
            .table(TABELA)
            .update(payload)
            .eq("id", id)
            .execute()
        )

        if not response.data:
            return jsonify({"erro": "Adolescente não encontrado"}), 404

        return jsonify(response.data[0]), 200

    except Exception as e:
        return jsonify({
            "erro": "Erro ao atualizar adolescente",
            "detalhes": str(e)
        }), 500


# ======================================================
# DELETAR
# ======================================================
@congregacoes_bp.route("/<int:id>", methods=["DELETE"])
def deletar(id):
    try:
        response = (
            supabase
            .table(TABELA)
            .delete()
            .eq("id", id)
            .execute()
        )

        if not response.data:
            return jsonify({"erro": "Adolescente não encontrado"}), 404

        return jsonify({"ok": True}), 200

    except Exception as e:
        return jsonify({
            "erro": "Erro ao deletar adolescente",
            "detalhes": str(e)
        }), 500
