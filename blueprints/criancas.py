from flask import Blueprint, request, jsonify
from db_config import connect_db

supabase = connect_db()

criancas_bp = Blueprint(
    "criancas",
    __name__,
    url_prefix="/criancas"
)

# ======================================================
# LISTAR TODOS
# ======================================================
@criancas_bp.route("/", methods=["GET"])
def listar():
    try:
        resp = (
            supabase
            .table("criancas")
            .select(
                "id, nome, nome_pai, nome_mae, cpf, contato, data_nasc, congregacao, endereco"
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
                "nome_pai": a.get("nome_pai"),
                "nome_mae": a.get("nome_mae"),
                "cpf": a.get("cpf"),
                "contato": a.get("contato"),
                "data_nasc": a.get("data_nasc"),
                "congregacao": a.get("congregacao"),
                "endereco": a.get("endereco") or {}
            })

        return jsonify(resultado), 200

    except Exception as e:
        print("ERRO LISTAR:", e)
        return jsonify([]), 200  # nunca quebra o front


# ======================================================
# CADASTRAR
# ======================================================
@criancas_bp.route("/", methods=["POST"])
def cadastrar():
    try:
        data = request.json

        endereco = data.get("endereco", {})

        nova = {
            "nome": data.get("nome"),
            "nome_pai": data.get("nome_pai"),
            "nome_mae": data.get("nome_mae"),
            "cpf": data.get("cpf"),
            "contato": data.get("contato"),
            "data_nasc": data.get("data_nasc"),
            "congregacao": data.get("congregacao"),
            "endereco": {
                "rua": endereco.get("rua"),
                "numero": endereco.get("numero"),
                "bairro": endereco.get("bairro")
            }
        }

        result = supabase.table("criancas").insert(nova).execute()
        if not result.data:
            return jsonify({"erro": "Erro ao inserir criança"}), 400

        return jsonify(result.data[0]), 201

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# ======================================================
# ATUALIZAR
# ======================================================
@criancas_bp.route("/<int:id>", methods=["PUT"])
def atualizar(id):
    try:
        data = request.json
        endereco = data.get("endereco", {})

        atualizada = {
            "nome": data.get("nome"),
            "nome_pai": data.get("nome_pai"),
            "nome_mae": data.get("nome_mae"),
            "cpf": data.get("cpf"),
            "contato": data.get("contato"),
            "data_nasc": data.get("data_nasc"),
            "congregacao": data.get("congregacao"),
            "endereco": {
                "rua": endereco.get("rua"),
                "numero": endereco.get("numero"),
                "bairro": endereco.get("bairro")
            }
        }

        resp = supabase.table("criancas").update(atualizada).eq("id", id).execute()
        if not resp.data:
            return jsonify({"erro": "Erro ao atualizar criança"}), 400

        return jsonify(resp.data[0]), 200


    except Exception as e:
        return jsonify({"erro": str(e)}), 500


# ======================================================
# DELETAR
# ======================================================
@criancas_bp.route("/<int:id>", methods=["DELETE"])
def deletar(id):
    try:
        supabase.table("criancas").delete().eq("id", id).execute()
        return jsonify({"ok": True}), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500
