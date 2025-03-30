document.addEventListener("DOMContentLoaded", function () {
    const dropdown = document.getElementById("companyDropdown");
    const detailsContainer = document.getElementById("companyDetails");

    async function fetchCompanyData(companyId) {
        if (!companyId) return;

        try {
            const response = await fetch(`/companies/${companyId}/`);
            if (!response.ok) throw new Error("Failed to fetch company data");

            const data = await response.json();

            const industry = Array.isArray(data.industry_list) ? data.industry_list.join(", ") : "N/A";

            const founders = Array.isArray(data.founders)
                ? data.founders.map(founder => `<span>${founder.name}</span>`).join(", ")
                : "N/A";

            const links = data.links && typeof data.links === "object"
                ? Object.entries(data.links)
                    .map(([name, url]) => {
                        if (!url) return "";
                        const fullUrl = url.startsWith("http") ? url : "https://" + url;
                        return `<a href="${fullUrl}" target="_blank">${name.charAt(0).toUpperCase() + name.slice(1)}</a>`;
                    })
                    .filter(link => link) // Remove empty links
                    .join(", ")
                : "N/A";

            function formatUrl(url) {
                return url ? (url.startsWith("http") ? url : "https://" + url) : "#";
            }

            // Build HTML with classes for styling
            detailsContainer.innerHTML = `
                <h2 class="company-title">${data.company_name}</h2>
                <div class="company-details company-detail__grid">
                    <div>
                        <p class="company-industry"><strong>Industry:</strong> ${industry}</p>
                        <p class="company-location"><strong>City:</strong> ${data.city} | <strong>State:</strong> ${data.state}</p>
                        <p class="company-founded"><strong>Founded:</strong> ${data.founded || "N/A"}</p>
                        <p class="company-website"><strong>Website:</strong> <a href="${formatUrl(data.website)}" target="_blank">${data.website || "N/A"}</a></p>
                        <p class="company-linkedin"><strong>LinkedIn:</strong> <a href="${formatUrl(data.linkedin)}" target="_blank">${data.linkedin || "N/A"}</a></p>
                    </div>
                    <div>
                        <p class="company-links"><strong>Links:</strong> ${links}</p>
                        <p class="company-description"><strong>Description:</strong> ${data.description || "No description available."}</p>
                        <p class="company-ownership"><strong>Company Ownership:</strong> ${data.company_ownership || "N/A"}</p>
                        <p class="company-founders"><strong>Founders:</strong> ${founders}</p>
                        <p class="company-ceo"><strong>CEO:</strong> ${data.ceo || "N/A"}</p>
                    </div>
                </div>
            `;

        } catch (error) {
            console.error("Error fetching company data:", error);
            detailsContainer.innerHTML = `<p style="color: red;">Error loading company details. Please try again.</p>`;
        }
    }

    dropdown.addEventListener("change", function () {
        fetchCompanyData(this.value);
    });

    if (dropdown.value) {
        fetchCompanyData(dropdown.value);
    }
});
