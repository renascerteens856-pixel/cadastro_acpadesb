@adolescentes_bp.get("/todos")
def listar_todos():
    try:
        supabase = connect_db()

        response = (
            supabase.table("adolescentes")
            .select("*")
            .order("id", desc=True)
            .execute()
        )

        # SDK novo → dict
        if response.get("error"):
            return jsonify({"erro": response["error"]["message"]}), 500

        return jsonify(response.get("data", [])), 200

    except Exception as e:
        return jsonify({"erro": "Erro ao listar todos", "detalhes": str(e)}), 500
