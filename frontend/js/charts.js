import { API_URL, formatCurrency } from './utils.js';

// Chart: Vendas por canal de venda
export async function loadChannelChart() {
    try {
        const response = await fetch(`${API_URL}/api/sales_by_channel`);
        const data = await response.json();

        const ctx = document.getElementById('channelChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.map(d => d.canal),
                datasets: [{
                    label: 'Faturamento (R$)',
                    data: data.map(d => d.faturamento),
                    backgroundColor: [
                        '#667eea',
                        '#764ba2',
                        '#f093fb',
                        '#4facfe',
                        '#43e97b',
                        '#fa709a',
                    ],
                    borderRadius: 8,
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: (context) => formatCurrency(context.parsed.y)
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: (value) => 'R$ ' + (value / 1000).toFixed(0) + 'k'
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Erro ao carregar gráfico de canais:', error);
    }
}

// Chart: Evolução de Vendas (timeline)
export async function loadTimelineChart() {
    try {
        const response = await fetch(`${API_URL}/api/sales-timeline?start=2025-01-01&end=2025-10-28`);
        const data = await response.json();

        console.log("📊 Dados timeline recebidos:", data);

        if (!Array.isArray(data) || data.length === 0) {
            console.warn("Nenhum dado retornado para o gráfico de timeline.");
            return;
        }

        const ctx = document.getElementById('timelineChart').getContext('2d');

        new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.map(d => d.data),
                datasets: [{
                    label: 'Vendas por Dia',
                    data: data.map(d => d.vendas),
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    tension: 0.4,
                    fill: true,
                    pointRadius: 0,
                    pointHoverRadius: 5
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: { 
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: (context) => `${context.parsed.y} vendas`
                        }
                    }
                },
                scales: {
                    x: { ticks: { maxTicksLimit: 10 } },
                    y: { 
                        beginAtZero: true,
                        ticks: {
                            callback: (value) => Math.floor(value)
                        }
                    }
                }
            }
        });

    } catch (error) {
        console.error('Erro no gráfico timeline:', error);
    }
}
export async function loadProductsChart() {
    const response = await fetch(`${API_URL}/api/top-products`);
    const data = await response.json();
    
    const ctx = document.getElementById('productsChart').getContext('2d');
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: data.map(d => d.produto),
            datasets: [{
                data: data.map(d => d.faturamento),
                backgroundColor: [
                    '#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b',
                    '#fa709a', '#fee140', '#30cfd0', '#a8edea', '#fed6e3'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'right'
                }
            }
        }
    });
}


loadProductsChart();

