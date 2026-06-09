// =====================
// THEME MANAGER
// =====================

// Apply saved theme when page loads
function applyTheme() {
    const saved = localStorage.getItem("toolverse-theme");
    if (saved === "light") {
        document.body.classList.add("light-mode");
        const btn = document.getElementById("themeBtn");
        if (btn) btn.textContent = "☀️";
    } else {
        document.body.classList.remove("light-mode");
        const btn = document.getElementById("themeBtn");
        if (btn) btn.textContent = "🌙";
    }
}

// Toggle between dark and light
function toggleTheme() {
    const isLight = document.body.classList.contains("light-mode");
    if (isLight) {
        document.body.classList.remove("light-mode");
        localStorage.setItem("toolverse-theme", "dark");
        document.getElementById("themeBtn").textContent = "🌙";
    } else {
        document.body.classList.add("light-mode");
        localStorage.setItem("toolverse-theme", "light");
        document.getElementById("themeBtn").textContent = "☀️";
    }
}

// Run on every page load
applyTheme();