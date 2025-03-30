document.addEventListener("DOMContentLoaded", function () {
    const dropdown = document.getElementById("companyDropdown");

    async function loadChartData(companyId) {
        if (!companyId) return;

        try {
            const cityResponse = await fetch(`/companies/${companyId}/job-distribution/`);
            const familyResponse = await fetch(`/companies/${companyId}/job-family-distribution/`);

            if (!cityResponse.ok || !familyResponse.ok) throw new Error("Failed to load chart data");

            const cityData = await cityResponse.json();
            const familyData = await familyResponse.json();

            if (cityData.cities && cityData.cities.length > 0) {
                renderCityChart(cityData.cities);
            } else {
                console.warn("No job distribution data available for cities.");
            }

            if (familyData.job_families && familyData.job_families.length > 0) {
                renderJobFamilyChart(familyData.job_families);
            } else {
                console.warn("No job distribution data available for job families.");
            }

        } catch (error) {
            console.error("Error loading charts:", error);
        }
    }

    function renderCityChart(cityData) {
        const chartDom = document.getElementById("cityChart");
        if (!chartDom) {
            console.error("City chart container not found!");
            return;
        }

        const myChart = echarts.init(chartDom);

        const option = {
            title: { text: "Job Distribution by City" },
            tooltip: { trigger: "axis" },
            xAxis: {
                type: "category",
                data: cityData.map(item => item.name),
                axisLabel: { rotate: 45 }, // Rotates labels for better visibility
            },
            yAxis: {
                type: "value",
                name: "Job Count",
            },
            series: [
                {
                    name: "Job Count",
                    type: "bar",
                    data: cityData.map(item => item.value),
                    itemStyle: {
                        color: "#007bff",
                        barBorderRadius: [5, 5, 0, 0],
                    },
                },
            ],
        };

        myChart.setOption(option);
    }

    function renderJobFamilyChart(jobFamilyData) {
        const chartDom = document.getElementById("jobFamilyChart");
        if (!chartDom) {
            console.error("Job Family chart container not found!");
            return;
        }

        const myChart = echarts.init(chartDom);

        const option = {
            title: { text: "Job Distribution by Role" },
            tooltip: { trigger: "item" },
            series: [
                {
                    name: "Job Count",
                    type: "pie",
                    radius: "50%",
                    data: jobFamilyData,
                },
            ],
        };

        myChart.setOption(option);
    }

    dropdown.addEventListener("change", function () {
        loadChartData(this.value);
    });

    // Load data for the first selected value (if any)
    if (dropdown.value) {
        loadChartData(dropdown.value);
    }
});
