// Small UI helper: prevent double submission while the local model is working.
document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("form").forEach((form) => {
        form.addEventListener("submit", (event) => {
            const submitter = event.submitter;
            if (!submitter) {
                return;
            }
            const loadingText = submitter.dataset.loadingText;
            if (loadingText) {
                submitter.textContent = loadingText;
                submitter.disabled = true;
            }
        });
    });
});
