from flask import Blueprint, request, jsonify
from supabase import create_client

# =========================
# CONFIGURAÇÃO SUPABASE
# =========================
SUPABASE_URL = "https://SEU_PROJETO.supabase.co"
SUPABASE_KEY = "SUA_SERVICE_ROLE_OU_ANON_KEY"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

adolescentes_bp = Blueprint("adolescentes", __name__, url_prefix="/adolescentes")

TABELA = "adolescentes"


# =========================
# FUNÇÃO AUXILIAR
# =========================
def normalizar_adolescente(item):
    """
    Garante que o JSON retornado
    esteja sempre no formato esperado pelo frontend
    """
    return {
        "id": item.get("id"),
        "nome": item.get("nome"),
        "nome_pai": item.get("nome_pai"),
        "nome_mae": item.get("nome_mae"),
        "contato": item.get("contato"),
        "data_nasc": item.get("data_nasc"),
        "endereco": item.get("endereco") or {
            "rua": "",
            "numero": "",
            "bairro": ""
        }
    }


# =========================
# LISTAR TODOS (GET)
# =========================
@adolescentes_bp.route("/", methods=["GET"])
def listar():
    try:
        response = supabase.table(TABELA).select("*").order("id", desc=False).execute()

        dados = response.data or []

        # SEMPRE retorna array
        adolescentes = [normalizar_adolescente(item) for item in dados]

        return jsonify(adolescentes), 200

    except Exception as e:
        return jsonify({
            "erro": "Erro ao listar adolescentes",
            "detalhes": str(e)
        }), 500


# =========================
# BUSCAR POR ID (GET)
# =========================
@adolescentes_bp.route("/<int:id>", methods=["GET"])
def buscar_por_id(id):
    try:
        response = (
            supabase
            .table(TABELA)
            .select("*")
            .eq("id", id)
            .single()
            .execute()
        )

        if not response.data:
            return jsonify({"erro": "Adolescente não encontrado"}), 404

        return jsonify(normalizar_adolescente(response.data)), 200

    except Exception as e:
        return jsonify({
            "erro": "Erro ao buscar adolescente",
            "detalhes": str(e)
        }), 500


# =========================
# CADASTRAR (POST)
# =========================
@adolescentes_bp.route("/", methods=["POST"])
def cadastrar():
    try:
        data = request.json or {}

        novo = {
            "nome": data.get("nome"),
            "nome_pai": data.get("nome_pai"),
            "nome_mae": data.get("nome_mae"),
            "contato": data.get("contato"),
            "data_nasc": data.get("data_nasc"),
            "endereco": data.get("endereco") or {
                "rua": "",
                "numero": "",
                "bairro": ""
            }
        }

        response = supabase.table(TABELA).insert(novo).execute()

        return jsonify({
            "mensagem": "Adolescente cadastrado com sucesso"
        }), 201

    except Exception as e:
        return jsonify({
            "erro": "Erro ao cadastrar adolescente",
            "detalhes": str(e)
        }), 500


# =========================
# ATUALIZAR (PUT)
# =========================
@adolescentes_bp.route("/<int:id>", methods=["PUT"])
def atualizar(id):
    try:
        data = request.json or {}

        atualizado = {
            "nome": data.get("nome"),
            "nome_pai": data.get("nome_pai"),
            "nome_mae": data.get("nome_mae"),
            "contato": data.get("contato"),
            "data_nasc": data.get("data_nasc"),
            "endereco": data.get("endereco") or {
                "rua": "",
                "numero": "",
                "bairro": ""
            }
        }

        supabase.table(TABELA).update(atualizado).eq("id", id).execute()

        return jsonify({
            "mensagem": "Adolescente atualizado com sucesso"
        }), 200

    except Exception as e:
        return jsonify({
            "erro": "Erro ao atualizar adolescente",
            "detalhes": str(e)
        }), 500


# =========================
# EXCLUIR (DELETE)
# =========================
@adolescentes_bp.route("/<int:id>", methods=["DELETE"])
def excluir(id):
    try:
        supabase.table(TABELA).delete().eq("id", id).execute()

        return jsonify({
            "mensagem": "Adolescente excluído com sucesso"
        }), 200

    except Exception as e:
        return jsonify({
            "erro": "Erro ao excluir adolescente",
            "detalhes": str(e)
        }), 500
