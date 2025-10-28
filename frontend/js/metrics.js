import { API_URL, formatCurrency, formatNumber } from './utils.js';

export async function loadMetrics() {
    try {
        const response = await fetch(`${API_URL}/api/overview`);

        if (!response.ok) {
            throw new Error('Erro ao buscar dados');
        }

        const data = await response.json();

        document.getElementById('metricsGrid').innerHTML = `
            <div class="metric-card">
                <div class="metric-label">Total de Vendas</div>
                <div class="metric-value">${formatNumber(data.total_vendas)}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Faturamento Total</div>
                <div class="metric-value">${formatCurrency(data.faturamento)}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Ticket Médio</div>
                <div class="metric-value">${formatCurrency(data.ticket_medio)}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Clientes Únicos</div>
                <div class="metric-value">${formatNumber(data.clientes_unicos)}</div>
            </div>
        `;
    } catch (error) {
        console.error('Erro:', error);
        document.getElementById('metricsGrid').innerHTML = `
            <div class="error">Erro ao carregar métricas. Verifique se a API está rodando.</div>
        `;
    }
}
