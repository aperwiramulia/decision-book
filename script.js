const revealTargets = document.querySelectorAll(
  ".goal-card, .method-card, .table-shell, .activity-card, .prompt-box, .download-card"
);

for (const element of revealTargets) {
  element.setAttribute("data-reveal", "");
}

const observer = new IntersectionObserver(
  (entries) => {
    for (const entry of entries) {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      }
    }
  },
  {
    threshold: 0.16,
    rootMargin: "0px 0px -40px 0px",
  }
);

for (const element of revealTargets) {
  observer.observe(element);
}