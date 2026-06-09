// =====================
// PAGE LOADER
// =====================

// Create loader element and inject into page
function createLoader() {
    const loader = document.createElement("div");
    loader.id = "pageLoader";
    loader.innerHTML = `
        <div class="loader-content">
            <div class="loader-logo">⚡</div>
            <div class="loader-text">ToolVerse</div>
            <div class="loader-spinner">
                <div class="spinner-ring"></div>
            </div>
        </div>
    `;
    document.body.appendChild(loader);
    return loader;
}

// Hide loader when page is ready
function hideLoader() {
    const loader = document.getElementById("pageLoader");
    if (loader) {
        loader.classList.add("loader-hide");
        setTimeout(() => loader.remove(), 600);
    }
}

// Show loader when navigating away
function showLoader() {
    const loader = document.getElementById("pageLoader");
    if (loader) {
        loader.classList.remove("loader-hide");
    } else {
        createLoader();
    }
}

// Create loader immediately when script loads
createLoader();

// Hide loader once page is fully loaded
window.addEventListener("load", () => {
    setTimeout(hideLoader, 300);
});

// Show loader when any navbar link is clicked
document.addEventListener("DOMContentLoaded", () => {
    const navLinks = document.querySelectorAll(".nav-link");
    navLinks.forEach(link => {
        link.addEventListener("click", (e) => {
            const href = link.getAttribute("href");
            if (href && href !== "#") {
                e.preventDefault();
                showLoader();
                setTimeout(() => {
                    window.location.href = href;
                }, 400);
            }
        });
    });
});