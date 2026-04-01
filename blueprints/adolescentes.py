from flask import Blueprint, request, jsonify
from db_config import connect_db
from datetime import datetime, date
import traceback

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
        supabase = connect_db()
        resp = supabase.table("adolescentes").select("*").order("nome").execute()
        return jsonify(resp.data or []), 200
    except Exception as e:
        print("ERRO LISTAR:", str(e))
        return jsonify([]), 200


# ======================================================
# BUSCAR POR NOME
# ======================================================
@adolescentes_bp.route("/buscar", methods=["GET"])
def buscar_por_nome():
    try:
        supabase = connect_db()
        nome = request.args.get("nome", "").strip()
        if not nome:
            return jsonify([]), 200
        resp = supabase.table("adolescentes").select("*").ilike("nome", f"%{nome}%").order("nome").execute()
        return jsonify(resp.data or []), 200
    except Exception as e:
        print("ERRO BUSCAR:", str(e))
        return jsonify([]), 200


# ======================================================
# CADASTRAR
# ======================================================
@adolescentes_bp.route("/", methods=["POST"])
def cadastrar():
    try:
        supabase = connect_db()
        data = request.json
        result = supabase.table("adolescentes").insert(data).execute()
        return jsonify(result.data[0]), 201
    except Exception as e:
        print("ERRO CADASTRAR:", str(e))
        return jsonify({"erro": str(e)}), 500


# ======================================================
# ATUALIZAR
# ======================================================
@adolescentes_bp.route("/<int:id>", methods=["PUT"])
def atualizar(id):
    try:
        supabase = connect_db()
        data = request.json
        resp = supabase.table("adolescentes").update(data).eq("id", id).execute()
        return jsonify(resp.data[0]), 200
    except Exception as e:
        print("ERRO ATUALIZAR:", str(e))
        return jsonify({"erro": str(e)}), 500


# ======================================================
# DELETAR
# ======================================================
@adolescentes_bp.route("/<int:id>", methods=["DELETE"])
def deletar(id):
    try:
        supabase = connect_db()
        supabase.table("adolescentes").delete().eq("id", id).execute()
        return jsonify({"ok": True}), 200
    except Exception as e:
        print("ERRO DELETAR:", str(e))
        return jsonify({"erro": str(e)}), 500


# ======================================================
# VERIFICAR E DELETAR MAIORES DE 18 ANOS
# ======================================================
@adolescentes_bp.route("/verificar-e-deletar-maiores", methods=["POST"])
def verificar_e_deletar_maiores():
    try:
        print("=" * 50)
        print("🚀 VERIFICANDO ADOLESCENTES > 18 ANOS")
        print("=" * 50)

        supabase = connect_db()

        resp = supabase.table("adolescentes").select("*").execute()
        adolescentes = resp.data or []
        print(f"📊 Adolescentes encontrados: {len(adolescentes)}")

        if not adolescentes:
            return jsonify({"status": "ok", "mensagem": "Nenhum adolescente", "deletados": 0}), 200

        hoje = date.today()
        deletados = []

        for adolescente in adolescentes:
            try:
                data_nasc_str = adolescente.get("data_nasc")
                if not data_nasc_str:
                    continue

                data_nasc = datetime.strptime(data_nasc_str, "%Y-%m-%d").date()
                idade = hoje.year - data_nasc.year
                if hoje.month < data_nasc.month or (hoje.month == data_nasc.month and hoje.day < data_nasc.day):
                    idade -= 1

                print(f"🔍 {adolescente.get('nome')} - Idade: {idade}")

                if idade > 18:
                    supabase.table("adolescentes").delete().eq("id", adolescente.get("id")).execute()
                    deletados.append({
                        "id": adolescente.get("id"),
                        "nome": adolescente.get("nome"),
                        "idade": idade
                    })
                    print(f"🗑️ DELETADO: {adolescente.get('nome')} ({idade} anos)")

            except Exception as e:
                print(f"❌ Erro: {e}")

        print(f"✅ TOTAL DELETADOS: {len(deletados)}")
        print("=" * 50)

        return jsonify({
            "status": "ok",
            "mensagem": f"{len(deletados)} adolescente(s) deletado(s)",
            "deletados": len(deletados),
            "deletados_lista": deletados
        }), 200

    except Exception as e:
        print("❌ ERRO:", str(e))
        traceback.print_exc()
        return jsonify({"status": "erro", "erro": str(e)}), 500
