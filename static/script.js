document.addEventListener("DOMContentLoaded", () => {
  // Keep form interactions small and predictable; server-side validation remains authoritative.
  const forms = document.querySelectorAll(".analysis-form");
  forms.forEach((form) => {
    form.addEventListener("submit", () => {
      const button = form.querySelector(".submit-button");
      if (button && form.checkValidity()) {
        button.disabled = true;
        button.innerHTML = "Analysing… <span>↗</span>";
      }
    });
  });

  // Subtle reveal effect, with a reduced-motion fallback.
  const revealTargets = document.querySelectorAll(".form-panel, .how-card, .roadmap-item");
  if ("IntersectionObserver" in window && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    revealTargets.forEach((element) => element.classList.add("reveal-ready"));
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("reveal-visible");
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.08 });
    revealTargets.forEach((element) => observer.observe(element));
  }
});
