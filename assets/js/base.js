$('[data-toggle="tooltip"]').tooltip();

function handleAnchorClick(event, anchor) {
  // write the full anchor URL to the clipboard
  navigator.clipboard.writeText(location.href.split("#")[0] + "#" + anchor);

  const anchorLink = document.getElementById("anchor-link-" + anchor);
  const copiedReaction = document.getElementById("copied-" + anchor);
  const copiedReactionText = document.getElementById(
    "copied-" + anchor + "-text",
  );

  // Add null checks before accessing properties
  if (anchorLink) {
    anchorLink.classList.add("force-visible");
  }

  if (copiedReaction) {
    copiedReaction.classList.add("visible");
    copiedReaction.style.display = "inline-block";
  }

  if (copiedReactionText) {
    copiedReactionText.textContent = "Copied!";
  }

  setTimeout(() => {
    if (anchorLink) {
      anchorLink.classList.remove("force-visible");
    }

    if (copiedReaction) {
      copiedReaction.classList.remove("visible");
      copiedReaction.style.display = "none";
    }

    if (copiedReactionText) {
      copiedReactionText.textContent = "";
    }
  }, 2000);
}
