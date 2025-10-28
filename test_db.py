import psycopg2

try:
    conn = psycopg2.connect(
        dbname="challenge_db",
        user="challenge",
        password="challenge_2024",
        host="localhost",
        port="5432"
    )
    print("Connection to the database was successful.")
    cur = conn.cursor()
    
    # --- QUERIES DE DIAGNÓSTICO ---
    print("-" * 30)
    print("Verificando status das vendas:")

    # 1. Quais são todos os status diferentes no banco e quantos existem de cada?
    cur.execute("SELECT sale_status_desc, COUNT(*) FROM sales GROUP BY sale_status_desc")
    statuses = cur.fetchall()
    print("Distribuição de todos os status:")
    if not statuses:
        print("  - NENHUM STATUS ENCONTRADO.")
    for status, count in statuses:
        print(f"  - '{status}': {count} vendas")

    # 2. Quantas vendas 'COMPLETED' existem no período correto?
    start_date = '2025-05-01'
    end_date = '2025-10-28'
    cur.execute(
        "SELECT COUNT(*) FROM sales WHERE sale_status_desc = 'COMPLETED' AND DATE(created_at) BETWEEN %s AND %s",
        (start_date, end_date)
    )
    completed_in_range = cur.fetchone()[0]
    print(f"\nVendas 'COMPLETED' no período ({start_date} a {end_date}): {completed_in_range}")
    print("-" * 30)
    
    cur.close()
    conn.close()
except Exception as e:
    print(f"An error occurred: {e}")