from flask import Blueprint, request, jsonify
from db_config import connect_db
from models.adolescente import Adolescente

adolescentes_bp = Blueprint("adolescentes", __name__)

# POST /adolescentes/  -> cadastrar
@adolescentes_bp.post("/")
def cadastrar():
    try:
        data = request.json or {}
        supabase = connect_db()

        # validação
        try:
            adolescente = Adolescente(**data)
        except Exception as e:
            return jsonify({"erro": "Dados inválidos", "detalhes": str(e)}), 400

        registro = {
            "nome": adolescente.nome,
            "nome_pai": adolescente.nome_pai,
            "nome_mae": adolescente.nome_mae,
            "contato": adolescente.contato,
            "data_nasc": adolescente.data_nasc,
            "endereco": adolescente.endereco
        }

        response = supabase.table("adolescentes").insert(registro).execute()
        if response.error:
            return jsonify({"erro": response.error.message}), 500

        return jsonify(response.data), 201

    except Exception as e:
        return jsonify({"erro": "Erro inesperado", "detalhes": str(e)}), 500


# GET simples: /adolescentes/todos -> retorna todos (ordenado por id desc)
@adolescentes_bp.get("/todos")
def listar_todos():
    try:
        supabase = connect_db()
        response = supabase.table("adolescentes").select("*").order("id", desc=True).execute()
        if response.error:
            return jsonify({"erro": response.error.message}), 500
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({"erro": "Erro ao listar todos", "detalhes": str(e)}), 500


# GET /adolescentes/buscar?nome=xxx
@adolescentes_bp.get("/buscar")
def buscar_por_nome():
    nome = request.args.get("nome")
    if not nome:
        return jsonify({"erro": "Parâmetro obrigatório: ?nome="}), 400

    try:
        supabase = connect_db()
        response = (
            supabase.table("adolescentes")
            .select("*")
            .filter("nome", "ilike", f"%{nome}%")
            .execute()
        )
        if response.error:
            return jsonify({"erro": response.error.message}), 500

        # se não houver dados, retorna lista vazia
        return jsonify(response.data or []), 200

    except Exception as e:
        return jsonify({"erro": "Erro ao buscar", "detalhes": str(e)}), 500


# PUT /adolescentes/<id>
@adolescentes_bp.put("/<int:adolescente_id>")
def atualizar(adolescente_id):
    try:
        data = request.json or {}
        supabase = connect_db()

        if not data:
            return jsonify({"erro": "Nenhum dado enviado"}), 400

        # reconstruir endereço se vier como campos soltos
        if not ("endereco" in data and isinstance(data["endereco"], dict)):
            endereco = {}
            if "bairro" in data:
                endereco["bairro"] = data["bairro"]
            if "cidade" in data:
                endereco["cidade"] = data["cidade"]
            if endereco:
                data["endereco"] = endereco
            data.pop("bairro", None)
            data.pop("cidade", None)

        response = supabase.table("adolescentes").update(data).eq("id", adolescente_id).execute()
        if response.error:
            return jsonify({"erro": response.error.message}), 400

        return jsonify(response.data), 200

    except Exception as e:
        return jsonify({"erro": "Erro ao atualizar", "detalhes": str(e)}), 500


# DELETE /adolescentes/<id>
@adolescentes_bp.delete("/<int:adolescente_id>")
def deletar(adolescente_id):
    try:
        supabase = connect_db()
        response = supabase.table("adolescentes").delete().eq("id", adolescente_id).execute()
        if response.error:
            return jsonify({"erro": response.error.message}), 400
        if not response.data:
            return jsonify({"erro": "Registro não encontrado"}), 404
        return jsonify({"mensagem": "Adolescente deletado com sucesso"}), 200
    except Exception as e:
        return jsonify({"erro": "Erro ao excluir", "detalhes": str(e)}), 500
