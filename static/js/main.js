document.addEventListener("DOMContentLoaded", () => {

    console.log("VisionAI Pro Loaded");

    initializeImagePreview();

    initRevealOnScroll();

    enforceSessionCloseLogout();

});

function initializeImagePreview() {

    const imageInput = document.getElementById("imageInput");

    if (!imageInput) {
        return;
    }

    imageInput.addEventListener("change", event => {

        const file = event.target.files[0];

        if (!file) {
            return;
        }

        const preview = document.getElementById("imagePreview");

        if (!preview) {
            return;
        }

        preview.src = URL.createObjectURL(file);

        preview.style.display = "block";

    });

}

function initRevealOnScroll() {

    const prefersReduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (prefersReduced) return;

    const items = document.querySelectorAll('[data-reveal="true"], .va-reveal');
    if (!items.length) return;

    const io = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-revealed');
                    io.unobserve(entry.target);
                }
            });
        },
        { threshold: 0.15 }
    );

    items.forEach((el) => io.observe(el));
}

function showLoading(buttonId) {

    const button = document.getElementById(buttonId);

    if (!button) {
        return;
    }

    button.innerHTML =
        '<span class="spinner-border spinner-border-sm"></span> Processing...';

    // Disable clicks without setting 'disabled=true' to ensure Chromium submissions are not cancelled
    button.style.pointerEvents = 'none';
    button.style.opacity = '0.75';

}

function resetButton(buttonId, text) {

    const button = document.getElementById(buttonId);

    if (!button) {
        return;
    }

    button.disabled = false;

    button.innerHTML = text;

}

// Admin logout: show signing-off screen animation and then redirect
(function adminLogoutHook() {

    if (typeof window === 'undefined') return;

    document.addEventListener('click', function (e) {
        const el = e.target && e.target.closest ? e.target.closest('[data-admin-logout="true"]') : null;
        if (!el) return;

        // Let the navigation happen, but show a small delay animation by forcing redirect to signoff
        // if href points to /admin/logout.
        const href = el.getAttribute('href');
        if (!href) return;

        if (href.includes('/admin/logout')) {
            e.preventDefault();
            window.location.href = href;
        }
    });
})();

function enforceSessionCloseLogout() {
    const logoutLink = document.querySelector('a[href*="logout"]');
    if (logoutLink) {
        const sessionActive = sessionStorage.getItem('va_session_active');
        if (!sessionActive) {
            window.location.href = logoutLink.href;
            return;
        }
    }

    document.addEventListener('submit', () => {
        sessionStorage.setItem('va_session_active', 'true');
    });
}

