document.addEventListener("DOMContentLoaded", () => {
    const chartElement = document.getElementById("accessChart");
    if (!chartElement) {
        return; 
    }

    const ctx = chartElement.getContext("2d");

    const COLORS = [
        "rgba(100, 255, 218, 0.6)",  
        "rgba(0, 191, 166, 0.6)",    
        "rgba(255, 206, 86, 0.6)",   
        "rgba(75, 192, 192, 0.6)",   
        "rgba(153, 102, 255, 0.6)",  
        "rgba(255, 99, 132, 0.6)"    
    ];

    let chart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: [],
            datasets: [{
                label: "Total de Acessos",
                data: [],
                backgroundColor: [],
                borderColor: "#00bfa6",
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false },
                title: {
                    display: true,
                    text: "Distribuição de Acessos por País",
                    color: "#64ffda",
                    font: { size: 20, weight: "bold" }
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            return `${context.label}: ${context.raw} acessos`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    ticks: { color: "#64ffda", font: { size: 14 } },
                    grid: { color: "#334155" }
                },
                y: {
                    ticks: { color: "#64ffda", font: { size: 14 } },
                    grid: { color: "#334155" }
                }
            },
            animation: {
                duration: 1200,
                easing: "easeOutBounce"
            }
        }
    });

    async function updateData() {
        try {
            const response = await fetch("/api/access-data/");
            const data = await response.json();

            chart.data.labels = data.map(item => item.country);
            chart.data.datasets[0].data = data.map(item => item.total);
            chart.data.datasets[0].backgroundColor = data.map((_, i) => COLORS[i % COLORS.length]);
            chart.update();

            const tableBody = document.getElementById("countryTableBody");
            if (tableBody) {
                tableBody.innerHTML = "";
                data.forEach(item => {
                    const row = document.createElement("tr");
                    row.innerHTML = `
                        <td>${item.country}</td>
                        <td>${item.total}</td>
                    `;
                    tableBody.appendChild(row);
                });
            }
        } catch (err) {
            console.error("Erro ao carregar dados:", err);
        }
    }

    updateData();
});
