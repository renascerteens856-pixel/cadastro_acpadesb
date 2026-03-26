from flask import Blueprint, request, jsonify
from db_config import connect_db
from datetime import datetime, date
import traceback

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
                "id, nome, nome_pai, nome_mae, cpf, rg, contato, data_nasc, congregacao, endereco"
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
                "rg": a.get("rg"),
                "contato": a.get("contato"),
                "data_nasc": a.get("data_nasc"),
                "congregacao": a.get("congregacao"),
                "endereco": a.get("endereco") or {}
            })

        return jsonify(resultado), 200

    except Exception as e:
        print("ERRO LISTAR:", e)
        return jsonify([]), 200


# ======================================================
# BUSCAR POR NOME
# ======================================================
@adolescentes_bp.route("/buscar", methods=["GET"])
def buscar_por_nome():
    try:
        nome = request.args.get("nome", "").strip()

        if not nome:
            return jsonify([]), 200

        resp = (
            supabase
            .table("adolescentes")
            .select(
                "id, nome, nome_pai, nome_mae, cpf, rg, contato, data_nasc, congregacao, endereco"
            )
            .ilike("nome", f"%{nome}%")
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
                "rg": a.get("rg"),
                "contato": a.get("contato"),
                "data_nasc": a.get("data_nasc"),
                "congregacao": a.get("congregacao"),
                "endereco": a.get("endereco") or {}
            })

        return jsonify(resultado), 200

    except Exception as e:
        print("ERRO BUSCAR:", e)
        return jsonify([]), 200


# ======================================================
# CADASTRAR
# ======================================================
@adolescentes_bp.route("/", methods=["POST"])
def cadastrar():
    try:
        data = request.get_json() or {}

        payload = {
            "nome": data.get("nome"),
            "nome_pai": data.get("nome_pai"),
            "nome_mae": data.get("nome_mae"),
            "cpf": data.get("cpf"),
            "rg": data.get("rg"),
            "contato": data.get("contato"),
            "data_nasc": data.get("data_nasc"),
            "congregacao": data.get("congregacao"),
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
            "nome_pai": data.get("nome_pai"),
            "nome_mae": data.get("nome_mae"),
            "cpf": data.get("cpf"),
            "rg": data.get("rg"),
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


# ======================================================
# VERIFICAR IDADE E DELETAR ADOLESCENTES COM MAIS DE 18 ANOS
# ======================================================
@adolescentes_bp.route("/verificar-e-deletar-maiores", methods=["POST"])
def verificar_e_deletar_maiores():
    """
    Verifica a idade de todos os adolescentes na tabela 'adolescentes'.
    Se a idade for maior que 18 anos, deleta o registro.
    """
    try:
        print("=" * 50)
        print("🔍 INICIANDO VERIFICAÇÃO DE ADOLESCENTES MAIORES DE 18 ANOS")
        print("=" * 50)

        # 1. Buscar todos os adolescentes
        resp = supabase.table("adolescentes").select("*").execute()
        adolescentes = resp.data or []

        if not adolescentes:
            print("ℹ️ Nenhum adolescente cadastrado.")
            return jsonify({
                "status": "ok",
                "mensagem": "Nenhum adolescente cadastrado",
                "total_analisados": 0,
                "deletados": 0,
                "deletados_lista": []
            }), 200

        print(f"📊 Total de adolescentes encontrados: {len(adolescentes)}")

        # 2. Calcular idade e separar os que devem ser deletados
        hoje = date.today()
        deletados_lista = []
        erros = []

        for adolescente in adolescentes:
            try:
                # Verificar se tem data de nascimento
                data_nasc_str = adolescente.get("data_nasc")
                if not data_nasc_str:
                    print(
                        f"⚠️ Adolescente ID {adolescente.get('id')} - {adolescente.get('nome')} sem data de nascimento, ignorado")
                    continue

                # Converter string para date
                if isinstance(data_nasc_str, str):
                    data_nasc = datetime.strptime(data_nasc_str, "%Y-%m-%d").date()
                else:
                    data_nasc = data_nasc_str

                # Calcular idade
                idade = hoje.year - data_nasc.year
                # Ajustar se ainda não fez aniversário este ano
                if hoje.month < data_nasc.month or (hoje.month == data_nasc.month and hoje.day < data_nasc.day):
                    idade -= 1

                print(f"🔍 {adolescente.get('nome')} - Data Nasc: {data_nasc} - Idade: {idade} anos")

                # Verificar se tem mais de 18 anos
                if idade > 18:
                    info_adolescente = {
                        "id": adolescente.get("id"),
                        "nome": adolescente.get("nome"),
                        "idade": idade,
                        "data_nasc": data_nasc_str,
                        "cpf": adolescente.get("cpf"),
                        "rg": adolescente.get("rg"),
                        "contato": adolescente.get("contato"),
                        "congregacao": adolescente.get("congregacao")
                    }

                    deletados_lista.append(info_adolescente)

                    # Deletar o registro
                    supabase.table("adolescentes").delete().eq("id", adolescente.get("id")).execute()
                    print(f"🗑️ DELETADO: {adolescente.get('nome')} (idade: {idade} anos)")

            except Exception as e:
                print(f"❌ Erro ao processar adolescente {adolescente.get('id')}: {e}")
                erros.append({
                    "id": adolescente.get("id"),
                    "nome": adolescente.get("nome", "Desconhecido"),
                    "erro": str(e)
                })

        # 3. Retornar resultado
        print("=" * 50)
        print(f"✅ VERIFICAÇÃO CONCLUÍDA: {len(deletados_lista)} adolescente(s) deletado(s)")
        print("=" * 50)

        return jsonify({
            "status": "ok",
            "mensagem": f"Verificação concluída. {len(deletados_lista)} adolescente(s) deletado(s) por terem mais de 18 anos.",
            "total_analisados": len(adolescentes),
            "deletados": len(deletados_lista),
            "deletados_lista": deletados_lista,
            "erros": erros
        }), 200

    except Exception as e:
        print("❌ ERRO NA VERIFICAÇÃO/DELECÃO:", str(e))
        traceback.print_exc()
        return jsonify({
            "status": "erro",
            "erro": str(e)
        }), 500


# ======================================================
# VERIFICAR IDADE (APENAS CONSULTA, SEM DELETAR)
# ======================================================
@adolescentes_bp.route("/verificar-idade", methods=["GET"])
def verificar_idade():
    """
    Apenas verifica a idade dos adolescentes e retorna quais seriam deletados.
    Não faz alterações no banco.
    """
    try:
        resp = supabase.table("adolescentes").select("*").execute()
        adolescentes = resp.data or []

        if not adolescentes:
            return jsonify({
                "status": "ok",
                "mensagem": "Nenhum adolescente cadastrado",
                "total_adolescentes": 0,
                "seriam_deletados": 0,
                "adolescentes": []
            }), 200

        hoje = date.today()
        resultado = []
        seriam_deletados = []

        for adolescente in adolescentes:
            try:
                data_nasc_str = adolescente.get("data_nasc")
                if not data_nasc_str:
                    resultado.append({
                        "id": adolescente.get("id"),
                        "nome": adolescente.get("nome"),
                        "data_nasc": None,
                        "idade": "N/A",
                        "seria_deletado": False,
                        "motivo": "Sem data de nascimento"
                    })
                    continue

                if isinstance(data_nasc_str, str):
                    data_nasc = datetime.strptime(data_nasc_str, "%Y-%m-%d").date()
                else:
                    data_nasc = data_nasc_str

                idade = hoje.year - data_nasc.year
                if hoje.month < data_nasc.month or (hoje.month == data_nasc.month and hoje.day < data_nasc.day):
                    idade -= 1

                seria_deletado = idade > 18

                item = {
                    "id": adolescente.get("id"),
                    "nome": adolescente.get("nome"),
                    "data_nasc": data_nasc_str,
                    "idade": idade,
                    "seria_deletado": seria_deletado,
                    "cpf": adolescente.get("cpf"),
                    "rg": adolescente.get("rg"),
                    "contato": adolescente.get("contato"),
                    "congregacao": adolescente.get("congregacao")
                }
                resultado.append(item)

                if seria_deletado:
                    seriam_deletados.append(item)

            except Exception as e:
                resultado.append({
                    "id": adolescente.get("id"),
                    "nome": adolescente.get("nome", "Desconhecido"),
                    "data_nasc": adolescente.get("data_nasc"),
                    "idade": "Erro",
                    "seria_deletado": False,
                    "erro": str(e)
                })

        return jsonify({
            "status": "ok",
            "total_adolescentes": len(adolescentes),
            "seriam_deletados": len(seriam_deletados),
            "adolescentes": resultado
        }), 200

    except Exception as e:
        print("ERRO AO VERIFICAR IDADE:", str(e))
        return jsonify({
            "status": "erro",
            "erro": str(e)
        }), 500
