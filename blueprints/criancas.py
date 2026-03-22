from flask import Blueprint, request, jsonify
from db_config import connect_db
from datetime import datetime, date
import traceback

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
@criancas_bp.route("/nome/<string:nome>", methods=["GET"])
def buscar_por_nome_exato(nome):
    try:
        resp = (
            supabase
            .table("criancas")
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
        print("ERRO BUSCAR POR NOME:", e)
        return jsonify({"erro": str(e)}), 500


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
            "rg": data.get("rg"),
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
            "rg": data.get("rg"),
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


# ======================================================
# VERIFICAR IDADE E MIGRAR PARA ADOLESCENTES
# ======================================================
@criancas_bp.route("/migrar-para-adolescentes", methods=["POST"])
def migrar_para_adolescentes():
    """
    Verifica a idade de todas as crianças na tabela 'criancas'.
    Se a idade for maior ou igual a 12 anos, move o registro para a tabela 'adolescentes'
    e remove da tabela 'criancas'.
    """
    try:
        # 1. Buscar todas as crianças
        resp = supabase.table("criancas").select("*").execute()
        criancas = resp.data or []

        if not criancas:
            return jsonify({
                "status": "ok",
                "mensagem": "Nenhuma criança cadastrada",
                "migradas": 0
            }), 200

        # 2. Calcular idade e separar as que devem ser migradas
        hoje = date.today()
        migradas = []
        erros = []

        for crianca in criancas:
            try:
                # Verificar se tem data de nascimento
                data_nasc_str = crianca.get("data_nasc")
                if not data_nasc_str:
                    print(f"⚠️ Criança {crianca.get('id')} sem data de nascimento, ignorada")
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

                print(f"🔍 Criança: {crianca.get('nome')} - Data Nasc: {data_nasc} - Idade: {idade} anos")

                # Verificar se tem 12 anos ou mais
                if idade >= 12:
                    # Preparar dados para adolescente (manter a mesma estrutura)
                    dados_adolescente = {
                        "nome": crianca.get("nome"),
                        "nome_pai": crianca.get("nome_pai"),
                        "nome_mae": crianca.get("nome_mae"),
                        "cpf": crianca.get("cpf"),
                        "rg": crianca.get("rg"),
                        "contato": crianca.get("contato"),
                        "data_nasc": crianca.get("data_nasc"),
                        "congregacao": crianca.get("congregacao"),
                        "endereco": crianca.get("endereco")  # Já está no formato JSONB
                    }

                    # Inserir na tabela adolescentes
                    insert_result = supabase.table("adolescentes").insert(dados_adolescente).execute()

                    if insert_result.data:
                        # Remover da tabela crianças
                        supabase.table("criancas").delete().eq("id", crianca.get("id")).execute()

                        migradas.append({
                            "id_original": crianca.get("id"),
                            "nome": crianca.get("nome"),
                            "idade": idade,
                            "novo_id": insert_result.data[0].get("id")
                        })
                        print(f"✅ Migrada: {crianca.get('nome')} (idade: {idade} anos)")
                    else:
                        erros.append({
                            "id": crianca.get("id"),
                            "nome": crianca.get("nome"),
                            "erro": "Falha ao inserir na tabela adolescentes"
                        })

            except Exception as e:
                print(f"❌ Erro ao processar criança {crianca.get('id')}: {e}")
                erros.append({
                    "id": crianca.get("id"),
                    "nome": crianca.get("nome", "Desconhecido"),
                    "erro": str(e)
                })

        # 3. Retornar resultado
        return jsonify({
            "status": "ok",
            "mensagem": f"Migração concluída. {len(migradas)} criança(s) migrada(s) para adolescentes.",
            "total_analisadas": len(criancas),
            "migradas": migradas,
            "erros": erros
        }), 200

    except Exception as e:
        print("ERRO NA MIGRAÇÃO:", str(e))
        traceback.print_exc()
        return jsonify({
            "status": "erro",
            "erro": str(e)
        }), 500


# ======================================================
# VERIFICAR IDADE (APENAS CONSULTA, SEM MIGRAR)
# ======================================================
@criancas_bp.route("/verificar-idade", methods=["GET"])
def verificar_idade():
    """
    Apenas verifica a idade das crianças e retorna quais seriam migradas.
    Não faz alterações no banco.
    """
    try:
        resp = supabase.table("criancas").select("*").execute()
        criancas = resp.data or []

        if not criancas:
            return jsonify({
                "status": "ok",
                "mensagem": "Nenhuma criança cadastrada",
                "criancas": []
            }), 200

        hoje = date.today()
        resultado = []
        seriam_migradas = []

        for crianca in criancas:
            try:
                data_nasc_str = crianca.get("data_nasc")
                if not data_nasc_str:
                    resultado.append({
                        "id": crianca.get("id"),
                        "nome": crianca.get("nome"),
                        "data_nasc": None,
                        "idade": "N/A",
                        "seria_migrada": False,
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

                seria_migrada = idade >= 12

                item = {
                    "id": crianca.get("id"),
                    "nome": crianca.get("nome"),
                    "data_nasc": data_nasc_str,
                    "idade": idade,
                    "seria_migrada": seria_migrada
                }
                resultado.append(item)

                if seria_migrada:
                    seriam_migradas.append(item)

            except Exception as e:
                resultado.append({
                    "id": crianca.get("id"),
                    "nome": crianca.get("nome", "Desconhecido"),
                    "data_nasc": crianca.get("data_nasc"),
                    "idade": "Erro",
                    "seria_migrada": False,
                    "erro": str(e)
                })

        return jsonify({
            "status": "ok",
            "total_criancas": len(criancas),
            "seriam_migradas": len(seriam_migradas),
            "criancas": resultado
        }), 200

    except Exception as e:
        print("ERRO AO VERIFICAR IDADE:", str(e))
        return jsonify({
            "status": "erro",
            "erro": str(e)
        }), 500
