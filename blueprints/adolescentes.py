from flask import Blueprint, request, jsonify
from db_config import connect_db

supabase = connect_db()

adolescentes_bp = Blueprint(
    "adolescentes",
    __name__,
    url_prefix="/adolescentes"
)

# ======================================================
# LISTAR TODOS
# ======================================================
@adolescentes_bp.route("/", methods=["GET"])
def listar():
    try:
        resp = (
            supabase
            .table("adolescentes")
            .select(
                "id, nome, cpf, contato, data_nasc, congregacao, endereco"
            )
            .order("nome")
            .execute()
        )

        dados = resp.data or []

        resultado = []
        for a in dados:
            resultado.append({
                "id": a.get("id"),
                "nome": a.get("nome"),
                "cpf": a.get("cpf"),
                "contato": a.get("contato"),
                "data_nasc": a.get("data_nasc"),
                "congregacao": a.get("congregacao"),  # ✅ AGORA FUNCIONA
                "endereco": a.get("endereco") or {}
            })

        return jsonify(resultado), 200

    except Exception as e:
        print("ERRO LISTAR:", e)
        return jsonify([]), 200  # nunca quebra o front


# ======================================================
# CADASTRAR
# ======================================================
@adolescentes_bp.route("/", methods=["POST"])
def cadastrar():
    try:
        data = request.get_json() or {}

        payload = {
            "nome": data.get("nome"),
            "cpf": data.get("cpf"),
            "contato": data.get("contato"),
            "data_nasc": data.get("data_nasc"),
            "congregacao": data.get("congregacao"),  # string
            "endereco": data.get("endereco")
        }

        resp = (
            supabase
            .table("adolescentes")
            .insert(payload)
            .execute()
        )

        return jsonify(resp.data[0]), 201

    except Exception as e:
        return jsonify({"erro": str(e)}), 500


# ======================================================
# ATUALIZAR
# ======================================================
@adolescentes_bp.route("/<int:id>", methods=["PUT"])
def atualizar(id):
    try:
        data = request.get_json() or {}

        payload = {
            "nome": data.get("nome"),
            "cpf": data.get("cpf"),
            "contato": data.get("contato"),
            "data_nasc": data.get("data_nasc"),
            "congregacao": data.get("congregacao"),
            "endereco": data.get("endereco")
        }

        resp = (
            supabase
            .table("adolescentes")
            .update(payload)
            .eq("id", id)
            .execute()
        )

        return jsonify(resp.data[0]), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500


# ======================================================
# DELETAR
# ======================================================
@adolescentes_bp.route("/<int:id>", methods=["DELETE"])
def deletar(id):
    try:
        supabase.table("adolescentes").delete().eq("id", id).execute()
        return jsonify({"ok": True}), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500
