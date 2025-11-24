from flask import Blueprint, request, jsonify
from db_config import connect_db

adolescente_bp = Blueprint("adolescente", __name__)


# =====================================================
# GET TODOS + BUSCA POR NOME
# =====================================================
@adolescente_bp.route("/adolescentes", methods=["GET"])
def get_all():
    try:
        nome = request.args.get("nome")

        supabase = connect_db()
        query = supabase.table("adolescentes").select("*")

        if nome:
            query = query.ilike("nome", f"%{nome}%")

        result = query.execute().data
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500


# =====================================================
# GET POR ID
# =====================================================
@adolescente_bp.route("/adolescentes/<int:id>", methods=["GET"])
def get_by_id(id):
    try:
        supabase = connect_db()
        result = (
            supabase.table("adolescentes")
            .select("*")
            .eq("id", id)
            .single()
            .execute()
        )

        return jsonify(result.data), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500


# =====================================================
# CRIAR ADOLESCENTE
# =====================================================
@adolescente_bp.route("/adolescentes", methods=["POST"])
def criar_adolescente():
    try:
        data = request.json
        supabase = connect_db()

        # Endereço é um TYPE
        endereco = {
            "rua": data.get("rua"),
            "numero": data.get("numero"),
            "bairro": data.get("bairro"),
        }

        payload = {
            "nome": data.get("nome"),
            "idade": data.get("idade"),
            "nome_pai": data.get("nome_pai"),
            "nome_mae": data.get("nome_mae"),
            "contato": data.get("contato"),
            "endereco": endereco,
        }

        resp = supabase.table("adolescentes").insert(payload).execute()
        return jsonify(resp.data), 201

    except Exception as e:
        return jsonify({"erro": str(e)}), 500


# =====================================================
# ATUALIZAR ADOLESCENTE
# =====================================================
@adolescente_bp.route("/adolescentes/<int:id>", methods=["PUT"])
def atualizar_adolescente(id):
    try:
        data = request.json
        supabase = connect_db()

        endereco = {
            "rua": data.get("rua"),
            "numero": data.get("numero"),
            "bairro": data.get("bairro"),
        }

        payload = {
            "nome": data.get("nome"),
            "idade": data.get("idade"),
            "nome_pai": data.get("nome_pai"),
            "nome_mae": data.get("nome_mae"),
            "contato": data.get("contato"),
            "endereco": endereco,
        }

        resp = (
            supabase.table("adolescentes")
            .update(payload)
            .eq("id", id)
            .execute()
        )

        return jsonify(resp.data), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500


# =====================================================
# DELETAR ADOLESCENTE
# =====================================================
@adolescente_bp.route("/adolescentes/<int:id>", methods=["DELETE"])
def deletar_adolescente(id):
    try:
        supabase = connect_db()

        existe = (
            supabase.table("adolescentes")
            .select("id")
            .eq("id", id)
            .execute()
        )

        if not existe.data:
            return jsonify({"erro": "Adolescente não encontrado"}), 404

        supabase.table("adolescentes").delete().eq("id", id).execute()

        return jsonify({"mensagem": "Registro deletado com sucesso"}), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500
