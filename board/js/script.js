// URL Backend (Harus sesuai dengan app.py yang berjalan di port 8000)
const API_DASHBOARD_URL = 'http://localhost:8000/dashboard-data'; 

let regressionChart, tempHistogramChart, revenueHistogramChart;

// --- FUNGSI UTAMA: MENGAMBIL DAN MERENDER DATA ---
async function fetchData() {
    try {
        const response = await fetch(API_DASHBOARD_URL);
        
        // 1. Cek Status HTTP (CORS, 404, 500)
        if (!response.ok) {
            // Coba baca respons sebagai teks untuk debugging error 404/500
            const errorText = await response.text();
            console.error("HTTP Error Status:", response.status);
            console.error("Server Response Text (for debugging):", errorText);
            throw new Error(`Failed to fetch data. Status: ${response.status}. Check server logs for details.`);
        }
        
        // 2. Cek JSON Parsing
        const data = await response.json();
        console.log("Data fetched successfully:", data); // Log data yang berhasil di-fetch
        
        // --- Cek Ketersediaan Data Kritis (untuk mencegah error rendering) ---
        if (!data.regression_data || !data.line_data) {
             throw new Error("Missing critical data (regression_data or line_data) in API response.");
        }

        // 3. Inisialisasi Visualisasi
        initializeCharts(
            data.regression_data, 
            data.line_data, 
            data.histogram_temp, 
            data.histogram_revenue
        );

        // 4. Isi Tabel
        populateMetrics(data.metrics);
        populateStatistics(data.stats_temp);
        
        // Sembunyikan loading, tampilkan konten
        document.getElementById('loading').classList.add('hidden');
        document.getElementById('main-content').classList.remove('hidden');

    } catch (error) {
        showError(error.message || 'Failed to fetch data. Check browser console for CORS/Network error details.');
        console.error("Final Fetch Error:", error);
    }
}

// =================================================================
// FUNGSI RENDERING CHART DAN TABEL (diambil dari solusi sebelumnya)
// =================================================================

function initializeCharts(regressionData, lineData, tempHist, revenueHist) {
    
    // Setup Skala Dinamis (Wajib untuk membuat grafik regresi terisi penuh)
    const tempValues = regressionData.map(d => d.temp);
    const revenueValues = regressionData.map(d => d.revenue);
    const minTemp = Math.min(...tempValues);
    const maxTemp = Math.max(...tempValues);
    const minRev = Math.min(...revenueValues);
    const maxRev = Math.max(...revenueValues);

    // 1. Grafik Regresi
    const regressionCtx = document.getElementById('regressionChart').getContext('2d');
    if (regressionChart) regressionChart.destroy(); // Cegah duplikasi chart
    regressionChart = new Chart(regressionCtx, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'Data Aktual',
                data: regressionData.map(d => ({ x: d.temp, y: d.revenue })),
                backgroundColor: '#ef4444',
                borderColor: '#ef4444',
                pointRadius: 5,
                pointHoverRadius: 7
            }, {
                label: 'Garis Regresi (Prediksi)',
                data: lineData,
                type: 'line',
                borderColor: '#0066CC',
                backgroundColor: 'transparent',
                borderWidth: 2,
                pointRadius: 0,
                tension: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: true, position: 'top', labels: { usePointStyle: true, padding: 15, font: { size: 11 } } },
                tooltip: { backgroundColor: 'white', titleColor: '#1e293b', bodyColor: '#1e293b', borderColor: '#e2e8f0', borderWidth: 1, padding: 10, displayColors: true }
            },
            scales: {
                x: {
                    title: { display: true, text: 'Temp (Suhu)', font: { size: 11 } },
                    min: minTemp - 2, 
                    max: maxTemp + 2, 
                    grid: { color: '#f1f5f9' }
                },
                y: {
                    title: { display: true, text: 'Rev (Pendapatan)', font: { size: 11 } },
                    min: minRev - 2, 
                    max: maxRev + 2, 
                    grid: { color: '#f1f5f9' }
                }
            }
        }
    });

    // 2. Histogram Temp
    const tempCtx = document.getElementById('tempHistogram').getContext('2d');
    if (tempHistogramChart) tempHistogramChart.destroy();
    tempHistogramChart = new Chart(tempCtx, {
        type: 'bar',
        data: {
            labels: tempHist.labels,
            datasets: [{ label: 'Frekuensi', data: tempHist.counts, backgroundColor: '#34d399', borderRadius: 4 }]
        },
        options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true, grid: { color: '#f1f5f9' } }, x: { grid: { display: false } } } }
    });

    // 3. Histogram Revenue
    const revenueCtx = document.getElementById('revenueHistogram').getContext('2d');
    if (revenueHistogramChart) revenueHistogramChart.destroy();
    revenueHistogramChart = new Chart(revenueCtx, {
        type: 'bar',
        data: {
            labels: revenueHist.labels,
            datasets: [{ label: 'Frekuensi', data: revenueHist.counts, backgroundColor: '#a3e635', borderRadius: 4 }]
        },
        options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true, grid: { color: '#f1f5f9' } }, x: { grid: { display: false } } } }
    });
}

function populateMetrics(metrics) {
    const metricsBody = document.getElementById('metricsBody');
    const metricsData = [
        { name: 'R² (Coefficient of Determination)', value: metrics.r2.toFixed(4) },
        { name: 'MAE (Mean Absolute Error)', value: metrics.mae.toFixed(4) },
        { name: 'MSE (Mean Squared Error)', value: metrics.mse.toFixed(4) },
        { name: 'RMSE (Root Mean Squared Error)', value: metrics.rmse.toFixed(4) },
        { name: 'Adj. R² (Adjusted R²)', value: metrics.r2_adj ? metrics.r2_adj.toFixed(4) : 'N/A' }
    ];
    
    metricsBody.innerHTML = metricsData.map(metric => `
        <tr><td>${metric.name}</td><td class="text-right">${metric.value}</td></tr>
    `).join('');
}

function populateStatistics(data) {
    const stats = data.stats_temp; 
    const statsGrid = document.getElementById('statsGrid');
    
    if (!stats) {
         statsGrid.innerHTML = `<p class="stats-label" style="grid-column: span 2;">Data statistik (Temp) tidak tersedia. Cek data EDA backend.</p>`;
         return;
    }

    statsGrid.innerHTML = `
        <div class="stats-section">
            <h3>Statistik Kuantil</h3>
            <div class="stats-row"><span class="stats-label">Mean:</span><span class="stats-value">${stats.mean.toFixed(2)}</span></div>
            <div class="stats-row"><span class="stats-label">Q1 (25%):</span><span class="stats-value">${stats['25%'].toFixed(2)}</span></div>
            <div class="stats-row"><span class="stats-label">Q2 (Median):</span><span class="stats-value">${stats['50%'].toFixed(2)}</span></div>
            <div class="stats-row"><span class="stats-label">Q3 (75%):</span><span class="stats-value">${stats['75%'].toFixed(2)}</span></div>
        </div>
        <div class="stats-section">
            <h3>Statistik Umum</h3>
            <div class="stats-row"><span class="stats-label">Min:</span><span class="stats-value">${stats.min.toFixed(2)}</span></div>
            <div class="stats-row"><span class="stats-label">Max:</span><span class="stats-value">${stats.max.toFixed(2)}</span></div>
            <div class="stats-row"><span class="stats-label">Std:</span><span class="stats-value">${stats.std.toFixed(2)}</span></div>
            <div class="stats-row"><span class="stats-label">Count:</span><span class="stats-value">${stats.count}</span></div>
        </div>
    `;
}

function showError(message) {
    document.getElementById('loading').classList.add('hidden');
    document.getElementById('error-message').textContent = message;
    document.getElementById('error').classList.remove('hidden');
}

window.addEventListener('load', fetchData);