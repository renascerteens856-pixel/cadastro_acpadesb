from flask import Blueprint, request, jsonify
from db_config import connect_db

supabase = connect_db()
TABELA = "congregacoes"

congregacoes_bp = Blueprint(
    "congregacoes",
    __name__,
    url_prefix="/congregacoes"
)

# =========================
# LISTAR TODOS
# =========================
@congregacoes_bp.route("/", methods=["GET"])
def listar():
    try:
        response = (
            supabase
            .table(TABELA)
            .select("id, nome")
            .order("nome")
            .execute()
        )

        return jsonify(response.data or []), 200

    except Exception as e:
        return jsonify({
            "erro": "Erro ao listar congregações",
            "detalhes": str(e)
        }), 500


# =========================
# BUSCAR UM
# =========================
@congregacoes_bp.route("/<int:id>", methods=["GET"])
def buscar(id):
    try:
        response = (
            supabase
            .table(TABELA)
            .select("id, nome")
            .eq("id", id)
            .single()
            .execute()
        )

        if not response.data:
            return jsonify({"erro": "Congregação não encontrada"}), 404

        return jsonify(response.data), 200

    except Exception as e:
        return jsonify({
            "erro": "Erro ao buscar congregação",
            "detalhes": str(e)
        }), 500


# =========================
# CADASTRAR
# =========================
@congregacoes_bp.route("/", methods=["POST"])
def cadastrar():
    try:
        data = request.get_json() or {}

        if not data.get("nome"):
            return jsonify({"erro": "Campo 'nome' é obrigatório"}), 400

        response = (
            supabase
            .table(TABELA)
            .insert({"nome": data["nome"]})
            .execute()
        )

        return jsonify(response.data[0]), 201

    except Exception as e:
        return jsonify({
            "erro": "Erro ao cadastrar congregação",
            "detalhes": str(e)
        }), 500


# =========================
# ATUALIZAR
# =========================
@congregacoes_bp.route("/<int:id>", methods=["PUT"])
def atualizar(id):
    try:
        data = request.get_json() or {}

        response = (
            supabase
            .table(TABELA)
            .update({"nome": data.get("nome")})
            .eq("id", id)
            .execute()
        )

        if not response.data:
            return jsonify({"erro": "Congregação não encontrada"}), 404

        return jsonify(response.data[0]), 200

    except Exception as e:
        return jsonify({
            "erro": "Erro ao atualizar congregação",
            "detalhes": str(e)
        }), 500


# =========================
# DELETAR
# =========================
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
            return jsonify({"erro": "Congregação não encontrada"}), 404

        return jsonify({"ok": True}), 200

    except Exception as e:
        return jsonify({
            "erro": "Erro ao deletar congregação",
            "detalhes": str(e)
        }), 500
