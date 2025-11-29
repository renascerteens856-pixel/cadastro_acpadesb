# adolescentes.py
from flask import Blueprint, request, jsonify
from db_config import connect_db

# ======================================================================
# CONFIGURAÇÃO DIRETA (sem .env)
# ======================================================================
      # service_role ou anon com policies liberadas

supabase = connect_db()

adolescentes_bp = Blueprint("adolescentes", __name__, url_prefix="/adolescentes")

# ======================================================================
# LISTAR TODOS
# ======================================================================
@adolescentes_bp.get("/")
def listar():
    try:
        resp = supabase.table("adolescentes").select("*").execute()
        return jsonify(resp.data), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


# ======================================================================
# BUSCAR 1
# ======================================================================
@adolescentes_bp.get("/<int:id>")
def buscar(id):
    try:
        resp = supabase.table("adolescentes").select("*").eq("id", id).single().execute()
        return jsonify(resp.data), 200
    except Exception as e:
        return jsonify({"erro": "Não encontrado", "detalhes": str(e)}), 404


# ======================================================================
# CADASTRAR
# ======================================================================
@adolescentes_bp.post("/")
def cadastrar():
    data = request.get_json()

    if not data or "nome" not in data:
        return jsonify({"erro": "campo 'nome' é obrigatório"}), 400

    try:
        resp = supabase.table("adolescentes").insert(data).execute()
        return jsonify(resp.data[0]), 201
    except Exception as e:
        return jsonify({"erro": "Erro ao inserir", "detalhes": str(e)}), 500


# ======================================================================
# ATUALIZAR
# ======================================================================
@adolescentes_bp.put("/<int:id>")
def atualizar(id):
    data = request.get_json()

    try:
        resp = supabase.table("adolescentes").update(data).eq("id", id).execute()
        if not resp.data:
            return jsonify({"erro": "Adolescente não encontrado"}), 404
        return jsonify(resp.data[0]), 200

    except Exception as e:
        return jsonify({"erro": "Erro ao atualizar", "detalhes": str(e)}), 500


# ======================================================================
# DELETAR
# ======================================================================
@adolescentes_bp.delete("/<int:id>")
def deletar(id):
    try:
        resp = supabase.table("adolescentes").delete().eq("id", id).execute()
        if not resp.data:
            return jsonify({"erro": "Adolescente não encontrado"}), 404

        return jsonify({"ok": True}), 200

    except Exception as e:
        return jsonify({"erro": "Erro ao deletar", "detalhes": str(e)}), 500
