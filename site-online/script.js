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

const downloadSearch = document.querySelector("#downloadSearch");

if (downloadSearch) {
  const downloadClear = document.querySelector("#downloadClear");
  const downloadToast = document.querySelector("#downloadToast");
  const downloadCards = Array.from(
    document.querySelectorAll(".downloads .download-card")
  );
  const downloadGroups = Array.from(
    document.querySelectorAll(".downloads .download-group")
  );
  const chipButtons = Array.from(
    document.querySelectorAll(".downloads [data-filter-chip]")
  );
  const emptyState = document.querySelector("#downloadEmpty");
  let visibleCardCount = 0;
  let toastTimer;

  const copyWithFallback = async (text) => {
    if (navigator.clipboard && window.isSecureContext) {
      try {
        await navigator.clipboard.writeText(text);
        return true;
      } catch {
        // Fall through to legacy copy.
      }
    }

    const hiddenInput = document.createElement("textarea");
    hiddenInput.value = text;
    hiddenInput.setAttribute("readonly", "");
    hiddenInput.style.position = "fixed";
    hiddenInput.style.opacity = "0";
    hiddenInput.style.pointerEvents = "none";
    document.body.appendChild(hiddenInput);
    hiddenInput.select();
    hiddenInput.setSelectionRange(0, hiddenInput.value.length);

    const copied = document.execCommand("copy");
    document.body.removeChild(hiddenInput);
    return copied;
  };

  for (const card of downloadCards) {
    const wrapper = document.createElement("div");
    wrapper.className = "download-item";
    card.parentNode?.insertBefore(wrapper, card);
    wrapper.appendChild(card);

    const actionStack = document.createElement("div");
    actionStack.className = "download-actions";

    const openLink = document.createElement("a");
    openLink.className = "download-action download-action--open";
    openLink.textContent = "Open";
    openLink.target = "_blank";
    openLink.rel = "noopener noreferrer";

    const copyBtn = document.createElement("button");
    copyBtn.type = "button";
    copyBtn.className = "download-action download-action--copy";
    copyBtn.textContent = "Copy link";
    copyBtn.setAttribute("aria-label", "Copy download link");

    copyBtn.addEventListener("click", async (event) => {
      event.preventDefault();
      event.stopPropagation();

      const href = card.getAttribute("href");
      if (!href) {
        return;
      }

      const absoluteUrl = new URL(href, window.location.href).href;
      openLink.href = absoluteUrl;

      try {
        const copied = await copyWithFallback(absoluteUrl);
        if (!copied) {
          throw new Error("Copy failed");
        }
        copyBtn.textContent = "Copied";
        showToast("Link copied");
      } catch {
        copyBtn.textContent = "Failed";
        showToast("Copy blocked");
      }

      window.setTimeout(() => {
        copyBtn.textContent = "Copy link";
      }, 1200);
    });

    const href = card.getAttribute("href");
    if (href) {
      openLink.href = new URL(href, window.location.href).href;
    }

    actionStack.appendChild(openLink);
    actionStack.appendChild(copyBtn);
    wrapper.appendChild(actionStack);
  }

  for (const group of downloadGroups) {
    const total = group.querySelectorAll(".download-card").length;
    group.dataset.totalCount = String(total);
  }

  const applyDownloadFilter = () => {
    const term = downloadSearch.value.toLowerCase().trim();
    visibleCardCount = 0;

    for (const card of downloadCards) {
      const haystack = `${card.textContent || ""} ${card.getAttribute("href") || ""}`
        .toLowerCase();
      const isMatch = term === "" || haystack.includes(term);
      const cardWrapper = card.closest(".download-item");
      if (cardWrapper) {
        cardWrapper.hidden = !isMatch;
      }
      if (isMatch) {
        visibleCardCount += 1;
      }
    }

    for (const group of downloadGroups) {
      const itemsInGroup = Array.from(group.querySelectorAll(".download-item"));
      const visibleInGroup = itemsInGroup.filter((item) => !item.hidden).length;
      group.hidden = visibleInGroup === 0;

      const badge = group.querySelector(".download-group__count");
      const totalInGroup = Number(group.dataset.totalCount || itemsInGroup.length);
      if (badge) {
        badge.textContent =
          term === ""
            ? `${totalInGroup} files`
            : `${visibleInGroup} of ${totalInGroup} files`;
      }
    }

    if (emptyState) {
      emptyState.hidden = visibleCardCount !== 0;
    }

    for (const chip of chipButtons) {
      const chipTerm = (chip.dataset.filterChip || "").toLowerCase();
      const isActive = chipTerm === term;
      chip.classList.toggle("is-active", isActive);
      chip.setAttribute("aria-pressed", String(isActive));
    }
  };

  const showToast = (label) => {
    if (!downloadToast) {
      return;
    }

    const suffix = visibleCardCount === 1 ? "1 file" : `${visibleCardCount} files`;
    downloadToast.textContent = `${label}: ${suffix}`;
    downloadToast.classList.add("is-visible");

    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => {
      if (downloadToast) {
        downloadToast.classList.remove("is-visible");
      }
    }, 1700);
  };

  downloadSearch.addEventListener("input", applyDownloadFilter);

  if (downloadClear) {
    downloadClear.addEventListener("click", () => {
      downloadSearch.value = "";
      applyDownloadFilter();
      showToast("Filter reset");
      downloadSearch.focus();
    });
  }

  for (const chip of chipButtons) {
    chip.addEventListener("click", () => {
      downloadSearch.value = chip.dataset.filterChip || "";
      applyDownloadFilter();
      const chipLabel = chip.textContent?.trim() || "Filter";
      showToast(`Filter ${chipLabel}`);
      downloadSearch.focus();
    });
  }

  document.addEventListener("keydown", (event) => {
    if (event.key !== "/") {
      return;
    }

    const activeTag = document.activeElement?.tagName?.toLowerCase() || "";
    const isTypingContext =
      activeTag === "input" ||
      activeTag === "textarea" ||
      activeTag === "select" ||
      document.activeElement?.isContentEditable;

    if (isTypingContext && document.activeElement !== downloadSearch) {
      return;
    }

    event.preventDefault();
    downloadSearch.focus();
    downloadSearch.select();
  });

  applyDownloadFilter();
}