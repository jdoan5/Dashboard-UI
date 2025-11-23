// Pick API base: local dev vs same-origin deploy
const API_BASE =
    (location.hostname === '127.0.0.1' || location.hostname === 'localhost')
        ? 'http://127.0.0.1:8000/api'
        : '/api';

const $error = document.getElementById('error');
function showError(msg) {
    if (!$error) return;
    $error.textContent = msg;
    $error.classList.remove('d-none');
}

async function getJSON(path) {
    const r = await fetch(`${API_BASE}${path}`);
    if (!r.ok) throw new Error(`${r.status} ${r.statusText} on ${path}`);
    return r.json();
}

function renderLowStock(rows) {
    const tbody = document.querySelector('#lowTable tbody');
    if (!tbody) return;

    // sort: most urgent first (on_hand - reorder_point ascending)
    rows.sort((a,b) => (a.on_hand - a.reorder_point) - (b.on_hand - b.reorder_point));

    tbody.innerHTML = rows.map(r => `
    <tr>
      <td>${r.sku}</td>
      <td>${r.name}</td>
      <td>${r.category}</td>
      <td class="text-end">${r.on_hand}</td>
      <td class="text-end">${r.reorder_point}</td>
    </tr>
  `).join('');
}

function renderSummary(rows) {
    const tbody = document.querySelector('#sumTable tbody');
    if (!tbody) return;

    rows.sort((a,b) => a.category.localeCompare(b.category));

    tbody.innerHTML = rows.map(r => `
    <tr>
      <td>${r.category}</td>
      <td class="text-end">${r.on_hand}</td>
      <td class="text-end">${r.reorder_total}</td>
    </tr>
  `).join('');
}

let salesChart;
function renderSalesChart(rows) {
    const ctx = document.getElementById('salesChart');
    if (!ctx) return;

    const labels = rows.map(r => r.category);
    const data = rows.map(r => r.sales_30d);

    if (salesChart) salesChart.destroy();
    salesChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels,
            datasets: [{
                label: 'Units sold (30d)',
                data
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                y: { beginAtZero: true, ticks: { precision:0 } }
            }
        }
    });
}

async function init() {
    try {
        const [sales, low, summary] = await Promise.all([
            getJSON('/sales_by_category'),
            getJSON('/low_stock'),
            getJSON('/inventory_summary'),
        ]);

        renderSalesChart(sales);
        renderLowStock(low);
        renderSummary(summary);
    } catch (e) {
        console.error(e);
        showError(`Failed to load data: ${e.message || e}`);
    }
}

document.addEventListener('DOMContentLoaded', init);