from flask import Blueprint, request, jsonify
from db_config import connect_db
from adolescente import Adolescente   # importa o modelo (Pydantic ou Dataclass)

adolescentes_bp = Blueprint("adolescentes", __name__)


@adolescentes_bp.post("/")
def cadastrar():
    data = request.json
    supabase = connect_db()
    # --- validar opção сom Pydantic (se estiver usando) ---
    try:
        adolescente = Adolescente(**data)
    except Exception as e:
        return jsonify({"erro": "Dados inválidos", "detalhes": str(e)}), 400

    # --- Inserir no Supabase ---
    response = supabase.table("adolescentes").insert({
        "nome": adolescente.nome,
        "nome_pai": adolescente.nome_pai,
        "nome_mae": adolescente.nome_mae,
        "idade": adolescente.idade,
        "endereco": adolescente.endereco,  # JSON funcionando
    }).execute()

    if response.error:
        return jsonify({"erro": response.error.message}), 500

    return jsonify(response.data), 201

@adolescentes_bp.get("/")
def listar():
    try:
        # ----- parâmetros opcionais -----
        pagina = int(request.args.get("pagina", 1))
        limite = int(request.args.get("limite", 20))
        ordenar_por = request.args.get("ordenar_por", "id")
        ordem = request.args.get("ordem", "desc")   # asc | desc
        supabase = connect_db()
        filtro_nome = request.args.get("nome")
        filtro_bairro = request.args.get("bairro")

        # ----- supabase query -----
        query = supabase.table("adolescentes").select("*")

        # filtro por nome (contém)
        if filtro_nome:
            query = query.ilike("nome", f"%{filtro_nome}%")

        # filtro por bairro (dentro do json)
        if filtro_bairro:
            query = query.ilike("endereco->>bairro", f"%{filtro_bairro}%")

        # ordenação
        query = query.order(ordenar_por, desc=(ordem == "desc"))

        # paginação
        inicio = (pagina - 1) * limite
        fim = inicio + limite - 1

        query = query.range(inicio, fim)

        # executar
        response = query.execute()

        if response.error:
            return jsonify({"erro": response.error.message}), 500

        # resposta estruturada
        return jsonify({
            "pagina": pagina,
            "limite": limite,
            "total": len(response.data),
            "dados": response.data
        }), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 400

@adolescentes_bp.get("/buscar")
def buscar_por_nome():
    nome = request.args.get("nome")
    supabase = connect_db()
    if not nome:
        return jsonify({"erro": "Você precisa informar o parâmetro ?nome="}), 400

    # Busca aproximada (contém)
    response = (
        supabase
        .table("adolescentes")
        .select("*")
        .ilike("nome", f"%{nome}%")
        .execute()
    )

    if response.error:
        return jsonify({"erro": response.error.message}), 500

    if not response.data:
        return jsonify({"mensagem": "Nenhum adolescente encontrado com esse nome"}), 404

    return jsonify(response.data), 200



@adolescentes_bp.put("/<int:adolescente_id>")
def atualizar(adolescente_id):
    data = request.json
    supabase = connect_db()
    # garante que atualizações vazias não quebrem o programa
    if not data:
        return jsonify({"erro": "Nenhum dado enviado"}), 400

    response = supabase.table("adolescentes").update(data).eq("id", adolescente_id).execute()

    if response.error:
        return jsonify({"erro": response.error.message}), 400

    return jsonify(response.data), 200

@adolescentes_bp.delete("/<int:adolescente_id>")
def deletar(adolescente_id):
    supabase = connect_db()
    response = supabase.table("adolescentes").delete().eq("id", adolescente_id).execute()

    if response.error:
        return jsonify({"erro": response.error.message}), 400

    # se deletou 0 registros
    if not response.data:
        return jsonify({"erro": "Adolescente não encontrado"}), 404

    return jsonify({"mensagem": "Adolescente deletado com sucesso"}), 200

