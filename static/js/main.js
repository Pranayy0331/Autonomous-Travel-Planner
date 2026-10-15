// Global JavaScript logic for Autonomous Travel Planner

document.addEventListener("DOMContentLoaded", function() {
    
    // --- 1. Dark/Light Theme Handler ---
    const themeToggleBtn = document.getElementById("themeToggleBtn");
    const htmlElement = document.documentElement;

    // Load initial theme choice from localStorage, defaulting to dark
    const savedTheme = localStorage.getItem("theme") || "dark";
    htmlElement.setAttribute("data-theme", savedTheme);

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener("click", function() {
            const currentTheme = htmlElement.getAttribute("data-theme");
            const newTheme = currentTheme === "dark" ? "light" : "dark";
            
            // Apply new theme state
            htmlElement.setAttribute("data-theme", newTheme);
            localStorage.setItem("theme", newTheme);
        });
    }

    // --- 2. Mobile Menu Toggler ---
    const mobileMenuBtn = document.getElementById("mobileMenuBtn");
    const navMenu = document.getElementById("navMenu");

    if (mobileMenuBtn && navMenu) {
        mobileMenuBtn.addEventListener("click", function() {
            navMenu.classList.toggle("active");
            
            // Switch hamburger/close icon
            const icon = mobileMenuBtn.querySelector("i");
            if (navMenu.classList.contains("active")) {
                icon.className = "fa-solid fa-xmark";
            } else {
                icon.className = "fa-solid fa-bars";
            }
        });
        
        // Close menu on click outside
        document.addEventListener("click", function(e) {
            if (!mobileMenuBtn.contains(e.target) && !navMenu.contains(e.target)) {
                navMenu.classList.remove("active");
                mobileMenuBtn.querySelector("i").className = "fa-solid fa-bars";
            }
        });
    }

    // --- 3. Alert / Toast Flash Messages Auto-dismiss ---
    const alerts = document.querySelectorAll(".alert");
    alerts.forEach(alert => {
        // Auto fade out after 5 seconds
        setTimeout(() => {
            alert.style.opacity = "0";
            alert.style.transform = "translateY(-10px)";
            alert.style.transition = "opacity 0.4s ease, transform 0.4s ease";
            setTimeout(() => {
                alert.remove();
            }, 400);
        }, 5000);
    });

});
