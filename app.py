from flask import Flask, jsonify, request
from flask_cors import CORS

import psycopg2
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)


DB_CONFIG = {
    'dbname': 'challenge_db',
    'user': 'challenge',
    'password': 'challenge_2024',
    'host': 'localhost',
    'port': '5432'
}

def get_db():
    """Establish a database connection."""
    return psycopg2.connect(**DB_CONFIG)

def format_decimal(value):
    """Format decimal values to two decimal places."""
    return float(value) if value else 0.0

@app.route('/')
def home():
    return jsonify({
        "message": 'API das analytics dos Restaurantes',
        'version': '1.0.0',
        'endpoints': [
            '/api/overview',
            '/api/sales_by_channel',
            '/api/sales-timeline',
        ]
    })
    
@app.route('/api/overview')
def overview():
    """Metricas gerais do negócio"""
    try:
        conn = get_db()
        cur = conn.cursor()
        
        #query principal
        cur.execute("""
            SELECT 
                COUNT(*) as total_vendas,
                SUM(total_amount)::numeric(15,2) as faturamento,
                AVG(total_amount)::numeric(15,2) as ticket_medio,
                COUNT(DISTINCT customer_id) as clientes_unicos,
                SUM(CASE WHEN sale_status_desc = 'CANCELLED' THEN 1 ELSE 0 END) as cancelamentos
            FROM sales
            WHERE sale_status_desc = 'COMPLETED'
        """)
        
        result = cur.fetchone()
        
        cur.execute("SELECT COUNT(*) FROM sales")
        total_all = cur.fetchone()[0]
        
        cur.close()
        conn.close()
        
        return jsonify({
            'total_vendas': result[0],
            'faturamento': format_decimal(result[1]),
            'ticket_medio': format_decimal(result[2]),
            'clientes_unicos': result[3],
            'taxa_cancelamento': round((result[4] / total_all) * 100, 2)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/sales_by_channel')
def sales_by_channel():
    """Vendas por canal de venda"""
    try:
        conn = get_db()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT 
                c.name as canal,
                c.type as tipo,
                COUNT(*) as vendas,
                SUM(s.total_amount)::numeric(10,2) as faturamento,
                AVG(s.total_amount)::numeric(10,2) as ticket_medio
            FROM sales s
            JOIN channels c ON c.id = s.channel_id
            WHERE s.sale_status_desc = 'COMPLETED'
            GROUP BY c.name, c.type
            ORDER BY faturamento DESC
        """)
        
        results = cur.fetchall()
        
        cur.close()
        conn.close()

        return jsonify([
            {
                'canal': row[0],
                'tipo': 'Delivery' if row[1] == 'D' else 'Presencial',
                'vendas': row[2],
                'faturamento': format_decimal(row[3]),
                'ticket_medio': format_decimal(row[4])
            }
            for row in results
        ])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/sales-timeline')
def sales_timeline():
    """Vendas ao longo do tempo"""
    try:
        # Parâmetros opcionais
        start_date = request.args.get('start', '2024-01-01')
        end_date = request.args.get('end', '2024-12-31')
        
        conn = get_db()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT 
                DATE(created_at) as dia,
                COUNT(*) as vendas,
                SUM(total_amount)::numeric(15,2) as faturamento
            FROM sales
            WHERE sale_status_desc = 'COMPLETED'
              AND DATE(created_at) BETWEEN %s AND %s
            GROUP BY dia
            ORDER BY dia
        """, (start_date, end_date))

        results = cur.fetchall()

        cur.close()
        conn.close()

        return jsonify([
            {
                'data': str(row[0]),
                'vendas': row[1],
                'faturamento': format_decimal(row[2])
            }
            for row in results
        ])
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    print("\n" + "="*50)
    print("Analytics dos Restaurantes - API!")
    print("="*50)
    print("Iniciando o servidor na porta 5000...")
    print("Endpoints disponíveis:")
    print(" GET /api/overview")
    print(" GET /api/sales_by_channel")
    print(" GET /api/sales-timeline?start=2025-05-01&end=2025-10-28")
    print("="*50 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
