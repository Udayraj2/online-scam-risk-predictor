let selectedApp = "Google Pay";

/* App selection */
document.querySelectorAll(".app-btn").forEach(btn => {
    btn.addEventListener("click", () => {
        selectedApp = btn.getAttribute("data-app");
        document.querySelectorAll(".app-btn").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
    });
});

/* Predict */
document.getElementById("predictBtn").addEventListener("click", async () => {
    const message = document.getElementById("messageInput").value.trim();
    const amount = parseInt(document.getElementById("amountInput").value);
    const sender_type = document.getElementById("senderType").value;

    if (!message || !amount) {
        alert("Please enter message and amount");
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:8000/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message, amount, sender_type })
        });

        const data = await response.json();

        const card = document.getElementById("resultCard");
        card.classList.remove("d-none");
        card.className = "alert p-3";

        /* Alert color */
        if (data.risk_level === "High Risk") {
            card.classList.add("alert-danger");
        } else if (data.risk_level === "Medium Risk") {
            card.classList.add("alert-warning");
        } else {
            card.classList.add("alert-success");
        }

        /* Result content */
        card.innerHTML = `
            <strong>${selectedApp} Prediction:</strong> ${data.prediction}<br>
            <strong>Risk Level:</strong> ${data.risk_level}<br>
            <strong>Confidence:</strong> ${Math.round((data.confidence || 0) * 100)}%<br><br>

            <strong>Why this transaction is risky:</strong>
            <ul>
                ${data.explanation.map(e => `<li>${e}</li>`).join("")}
            </ul>
        `;

        /* Show disclaimer */
        document.getElementById("disclaimer").classList.remove("d-none");

    } catch (err) {
        alert("Server error. Please try again.");
        console.error(err);
    }
});
