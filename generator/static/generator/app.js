// Small UI helper: prevent double submission while the local model is working.
document.addEventListener("DOMContentLoaded", () => {
    let progressTimer = null;
    let scriptFormAlreadySubmitting = false;

    const startEstimatedProgress = () => {
        const statusPanel = document.getElementById("script-generation-status");
        const progressText = document.getElementById("script-progress-percent");
        const progressBar = document.getElementById("script-progress-bar");
        if (!statusPanel || !progressText || !progressBar) {
            return;
        }

        statusPanel.hidden = false;
        statusPanel.scrollIntoView({ behavior: "smooth", block: "start" });

        let progressValue = 0;
        progressText.textContent = "0%";
        progressBar.style.width = "0%";

        if (progressTimer) {
            clearInterval(progressTimer);
        }

        progressTimer = setInterval(() => {
            if (progressValue < 60) {
                progressValue += 4;
            } else if (progressValue < 85) {
                progressValue += 2;
            } else if (progressValue < 95) {
                progressValue += 1;
            }

            progressValue = Math.min(progressValue, 95);
            progressText.textContent = `${progressValue}%`;
            progressBar.style.width = `${progressValue}%`;
        }, 1200);
    };

    document.querySelectorAll("form").forEach((form) => {
        form.addEventListener("submit", (event) => {
            const submitter = event.submitter;
            if (!submitter) {
                return;
            }
            if (submitter.name === "generate") {
                if (scriptFormAlreadySubmitting) {
                    return;
                }
                event.preventDefault();
                scriptFormAlreadySubmitting = true;
                startEstimatedProgress();
                const loadingText = submitter.dataset.loadingText;
                if (loadingText) {
                    submitter.textContent = loadingText;
                    submitter.disabled = true;
                }
                window.setTimeout(() => {
                    form.requestSubmit(submitter);
                }, 250);
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
