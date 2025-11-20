from db_config import connect_db
from flask import jsonify, request, Blueprint

adolescente_bp = Blueprint("adolescente", __name__)

# ---------------------------
# GET TODOS
# ---------------------------
@adolescente_bp.route("/adolescentes", methods=["GET"])
def get_all():
    try:
        nome = request.args.get("nome")

        supabase = connect_db()
        query = supabase.table("adolescentes").select("*")

        # GET por nome via querystring
        if nome:
            query = query.ilike("nome", f"%{nome}%")

        data = query.execute().data
        return jsonify(data), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500


# ---------------------------
# GET POR ID
# ---------------------------
@adolescente_bp.route("/adolescentes/<int:id>", methods=["GET"])
def get_by_id(id):
    try:
        supabase = connect_db()
        response = (
            supabase.table("adolescentes")
            .select("*")
            .eq("id", id)
            .single()
            .execute()
        )

        return jsonify(response.data), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500


# ---------------------------
# CREATE
# ---------------------------
@adolescente_bp.route("/adolescentes", methods=["POST"])
def create_adolescente():
    try:
        data = request.json

        supabase = connect_db()
        response = supabase.table("adolescentes").insert(data).execute()

        return jsonify(response.data), 201

    except Exception as e:
        return jsonify({"erro": str(e)}), 500


# ---------------------------
# UPDATE (PUT)
# ---------------------------
@adolescente_bp.route("/adolescentes/<int:id>", methods=["PUT"])
def update_adolescente(id):
    try:
        data = request.json

        supabase = connect_db()
        response = (
            supabase.table("adolescentes")
            .update(data)
            .eq("id", id)
            .execute()
        )

        return jsonify(response.data), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@adolescente_bp.route("/adolescentes/<int:id>", methods=["DELETE"])
def deletar_adolescente(id):
    try:
        supabase = connect_db()

        # Verifica se existe antes de deletar
        check = supabase.table("adolescentes").select("*").eq("id", id).execute()

        if not check.data:
            return jsonify({"erro": "Adolescente não encontrado"}), 404

        # Deleta o registro
        response = (
            supabase.table("adolescentes")
            .delete()
            .eq("id", id)
            .execute()
        )

        return jsonify({"mensagem": "Adolescente deletado com sucesso!"}), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500