document.addEventListener("DOMContentLoaded", () => {
  const capabilitiesList = document.getElementById("capabilities-list");
  const capabilitySelect = document.getElementById("capability");
  const matchingCapabilitySelect = document.getElementById("matching-capability");
  const matchingForm = document.getElementById("matching-form");
  const topNInput = document.getElementById("top-n");
  const recommendationsList = document.getElementById("recommendations-list");
  const registerForm = document.getElementById("register-form");
  const messageDiv = document.getElementById("message");

  // Function to fetch capabilities from API
  async function fetchCapabilities() {
    try {
      const response = await fetch("/capabilities");
      const capabilities = await response.json();

      // Clear loading message
      capabilitiesList.innerHTML = "";

      // Populate capabilities list
      capabilitySelect.innerHTML = '<option value="">-- Select a capability --</option>';
      matchingCapabilitySelect.innerHTML = '<option value="">-- Select a capability --</option>';

      Object.entries(capabilities).forEach(([name, details]) => {
        const capabilityCard = document.createElement("div");
        capabilityCard.className = "capability-card";

        const availableCapacity = details.capacity || 0;
        const currentConsultants = details.consultants ? details.consultants.length : 0;

        // Create consultants HTML with delete icons
        const consultantsHTML =
          details.consultants && details.consultants.length > 0
            ? `<div class="consultants-section">
              <h5>Registered Consultants:</h5>
              <ul class="consultants-list">
                ${details.consultants
                  .map(
                    (email) =>
                      `<li><span class="consultant-email">${email}</span><button class="delete-btn" data-capability="${name}" data-email="${email}">❌</button></li>`
                  )
                  .join("")}
              </ul>
            </div>`
            : `<p><em>No consultants registered yet</em></p>`;

        capabilityCard.innerHTML = `
          <h4>${name}</h4>
          <p>${details.description}</p>
          <p><strong>Practice Area:</strong> ${details.practice_area}</p>
          <p><strong>Industry Verticals:</strong> ${details.industry_verticals ? details.industry_verticals.join(', ') : 'Not specified'}</p>
          <p><strong>Capacity:</strong> ${availableCapacity} hours/week available</p>
          <p><strong>Current Team:</strong> ${currentConsultants} consultants</p>
          <div class="consultants-container">
            ${consultantsHTML}
          </div>
        `;

        capabilitiesList.appendChild(capabilityCard);

        // Add option to select dropdown
        const option = document.createElement("option");
        option.value = name;
        option.textContent = name;
        capabilitySelect.appendChild(option);

        const matchingOption = document.createElement("option");
        matchingOption.value = name;
        matchingOption.textContent = name;
        matchingCapabilitySelect.appendChild(matchingOption);
      });

      // Add event listeners to delete buttons
      document.querySelectorAll(".delete-btn").forEach((button) => {
        button.addEventListener("click", handleUnregister);
      });
    } catch (error) {
      capabilitiesList.innerHTML =
        "<p>Failed to load capabilities. Please try again later.</p>";
      console.error("Error fetching capabilities:", error);
    }
  }

  function renderRecommendations(payload) {
    const recommendations = payload.recommendations || [];

    if (recommendations.length === 0) {
      recommendationsList.innerHTML = "<p><em>No available consultants to recommend for this capability.</em></p>";
      return;
    }

    const cardsHTML = recommendations
      .map((item, index) => {
        const explain = item.explainability || {};
        return `
          <article class="recommendation-card">
            <h4>#${index + 1} ${item.name}</h4>
            <p><strong>Email:</strong> ${item.email}</p>
            <p><strong>Match Score:</strong> ${item.score} / 100</p>
            <div class="explainability-grid">
              <p><strong>Skill:</strong> ${explain.skill_level?.points || 0} pts (${explain.skill_level?.reason || "N/A"})</p>
              <p><strong>Certifications:</strong> ${explain.certifications?.points || 0} pts (${explain.certifications?.reason || "N/A"})</p>
              <p><strong>Availability:</strong> ${explain.availability?.points || 0} pts (${explain.availability?.reason || "N/A"})</p>
              <p><strong>Practice Area:</strong> ${explain.practice_area?.points || 0} pts (${explain.practice_area?.reason || "N/A"})</p>
              <p><strong>Industry:</strong> ${explain.industry_overlap?.points || 0} pts (${explain.industry_overlap?.reason || "N/A"})</p>
            </div>
          </article>
        `;
      })
      .join("");

    recommendationsList.innerHTML = cardsHTML;
  }

  matchingForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const capability = matchingCapabilitySelect.value;
    const topN = topNInput.value;

    try {
      const response = await fetch(
        `/capabilities/${encodeURIComponent(capability)}/recommendations?top_n=${encodeURIComponent(topN)}`
      );
      const result = await response.json();

      if (!response.ok) {
        recommendationsList.innerHTML = `<p class="error">${result.detail || "Failed to load recommendations."}</p>`;
        return;
      }

      renderRecommendations(result);
    } catch (error) {
      recommendationsList.innerHTML = "<p class=\"error\">Failed to load recommendations. Please try again.</p>";
      console.error("Error fetching recommendations:", error);
    }
  });

  // Handle unregister functionality
  async function handleUnregister(event) {
    const button = event.target;
    const capability = button.getAttribute("data-capability");
    const email = button.getAttribute("data-email");

    try {
      const response = await fetch(
        `/capabilities/${encodeURIComponent(
          capability
        )}/unregister?email=${encodeURIComponent(email)}`,
        {
          method: "DELETE",
        }
      );

      const result = await response.json();

      if (response.ok) {
        messageDiv.textContent = result.message;
        messageDiv.className = "success";

        // Refresh capabilities list to show updated consultants
        fetchCapabilities();
      } else {
        messageDiv.textContent = result.detail || "An error occurred";
        messageDiv.className = "error";
      }

      messageDiv.classList.remove("hidden");

      // Hide message after 5 seconds
      setTimeout(() => {
        messageDiv.classList.add("hidden");
      }, 5000);
    } catch (error) {
      messageDiv.textContent = "Failed to unregister. Please try again.";
      messageDiv.className = "error";
      messageDiv.classList.remove("hidden");
      console.error("Error unregistering:", error);
    }
  }

  // Handle form submission
  registerForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const capability = document.getElementById("capability").value;

    try {
      const response = await fetch(
        `/capabilities/${encodeURIComponent(
          capability
        )}/register?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
        messageDiv.textContent = result.message;
        messageDiv.className = "success";
        registerForm.reset();

        // Refresh capabilities list to show updated consultants
        fetchCapabilities();
      } else {
        messageDiv.textContent = result.detail || "An error occurred";
        messageDiv.className = "error";
      }

      messageDiv.classList.remove("hidden");

      // Hide message after 5 seconds
      setTimeout(() => {
        messageDiv.classList.add("hidden");
      }, 5000);
    } catch (error) {
      messageDiv.textContent = "Failed to register. Please try again.";
      messageDiv.className = "error";
      messageDiv.classList.remove("hidden");
      console.error("Error registering:", error);
    }
  });

  // Initialize app
  fetchCapabilities();
});
