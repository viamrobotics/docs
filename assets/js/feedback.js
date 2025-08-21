class FeedbackSystem {
  constructor() {
    this.isActive = false;
    this.isHighlighting = false;
    this.startX = 0;
    this.startY = 0;
    this.currentSelection = null;
    this.highlightedElements = [];

    this.init();
  }

  init() {
    this.bindEvents();
  }

  bindEvents() {
    // Feedback button click
    const feedbackBtn = document.getElementById("feedbackButtonToc");
    if (feedbackBtn) {
      feedbackBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        this.toggleFeedbackForm();
      });
    }

    // Clickable highlight status area
    const highlightStatus = document.getElementById("feedbackHighlightStatus");
    if (highlightStatus) {
      highlightStatus.addEventListener("click", (e) => {
        e.stopPropagation();
        if (!this.isHighlighting) {
          this.startHighlightingMode();
        }
      });
    }

    // Done highlighting button
    const doneHighlightBtn = document.getElementById("highlightingModeDone");
    if (doneHighlightBtn) {
      doneHighlightBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        this.stopHighlightingMode();
      });
    }

    // Submit button
    const submitBtn = document.getElementById("feedbackSubmit");
    if (submitBtn) {
      submitBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        this.submitFeedback();
      });
    }
  }

  toggleFeedbackForm() {
    const form = document.getElementById("feedbackForm");
    const button = document.getElementById("feedbackButtonToc");

    if (form.style.display === "none") {
      this.showFeedbackForm();
    } else {
      this.hideFeedbackForm();
    }
  }

  showFeedbackForm() {
    const form = document.getElementById("feedbackForm");
    const button = document.getElementById("feedbackButtonToc");

    if (form) {
      form.style.display = "block";
    }

    if (button) {
      button.innerHTML =
        '<span><i class="fas fa-times fa-sm" style="margin-right: 0.5rem"></i>Cancel Feedback</span>';
      button.classList.add("feedback-active");
    }
  }

  hideFeedbackForm() {
    const form = document.getElementById("feedbackForm");
    const button = document.getElementById("feedbackButtonToc");

    if (form) {
      form.style.display = "none";
    }

    if (button) {
      button.innerHTML =
        '<span><i class="fas fa-comment-dots fa-sm" style="margin-right: 0.5rem"></i>Give Feedback</span>';
      button.classList.remove("feedback-active");
    }

    // Stop highlighting mode if active
    this.stopHighlightingMode();

    // Reset form
    this.resetForm();
  }

  startHighlightingMode() {
    // Show the highlighting mode indicator
    const indicator = document.getElementById("highlightingModeIndicator");
    if (indicator) {
      indicator.classList.add("show");
    }

    // Enable page highlighting
    this.enablePageHighlighting();

    // Update the highlight status to show it's active
    this.updateHighlightStatusActive();

    // Remove clickable styling
    const highlightStatus = document.getElementById("feedbackHighlightStatus");
    if (highlightStatus) {
      highlightStatus.classList.remove("clickable");
    }
  }

  stopHighlightingMode() {
    // Hide the highlighting mode indicator
    const indicator = document.getElementById("highlightingModeIndicator");
    if (indicator) {
      indicator.classList.remove("show");
    }

    // Disable page highlighting
    this.disablePageHighlighting();

    // Update the highlight status to show selected elements
    this.updateHighlightStatusWithSelection();

    // Restore clickable styling if no elements are selected
    if (this.highlightedElements.length === 0) {
      const highlightStatus = document.getElementById(
        "feedbackHighlightStatus",
      );
      if (highlightStatus) {
        highlightStatus.classList.add("clickable");
      }
    }
  }

  enablePageHighlighting() {
    this.isActive = true;
    this.isHighlighting = true;
    document.body.classList.add("feedback-highlight-active");

    // Add click event listeners to all clickable elements
    this.addHighlightListeners();
  }

  disablePageHighlighting() {
    this.isActive = false;
    this.isHighlighting = false;
    document.body.classList.remove("feedback-highlight-active");

    // Remove all highlight event listeners
    this.removeHighlightListeners();

    // Reset cursor to normal
    document.body.style.cursor = "";
  }

  addHighlightListeners() {
    // Add click listeners to all elements that can be highlighted
    // EXCLUDE the feedback form elements to prevent them from being highlighted
    const highlightableElements = document.querySelectorAll(
      "p, h1, h2, h3, h4, h5, h6, li, div, span, img, code, pre, table, tr, td, th",
    );

    highlightableElements.forEach((element) => {
      if (element.offsetWidth > 0 && element.offsetHeight > 0) {
        // Skip elements that are part of the feedback form
        if (this.isFeedbackFormElement(element)) {
          return;
        }

        // Store the bound function reference so we can remove it later
        const boundHandler = (e) => this.highlightElement(e, element);
        element._feedbackHighlightHandler = boundHandler;
        element.addEventListener("click", boundHandler);
      }
    });
  }

  removeHighlightListeners() {
    const highlightableElements = document.querySelectorAll(
      "p, h1, h2, h3, h4, h5, h6, li, div, span, img, code, pre, table, tr, td, th",
    );

    highlightableElements.forEach((element) => {
      if (element._feedbackHighlightHandler) {
        element.removeEventListener("click", element._feedbackHighlightHandler);
        delete element._feedbackHighlightHandler;
      }
    });
  }

  isFeedbackFormElement(element) {
    // Check if the element is part of the feedback form
    const feedbackForm = document.getElementById("feedbackForm");
    const feedbackButton = document.getElementById("feedbackButtonToc");

    if (!feedbackForm || !feedbackButton) {
      return false;
    }

    // Check if element is inside the feedback form
    if (feedbackForm.contains(element)) {
      return true;
    }

    // Check if element is the feedback button
    if (element === feedbackButton) {
      return true;
    }

    // Check if element is inside the feedback button
    if (feedbackButton.contains(element)) {
      return true;
    }

    return false;
  }

  highlightElement(e, element) {
    // Only process if we're actually in highlighting mode
    if (!this.isHighlighting) {
      return;
    }

    e.preventDefault();
    e.stopPropagation();

    // Remove previous highlights
    this.clearHighlights();

    // Add highlight to current element
    element.classList.add("feedback-highlight-selected");
    this.highlightedElements.push(element);

    // Automatically stop highlighting mode after element selection
    this.stopHighlightingMode();
  }

  clearHighlights() {
    this.highlightedElements.forEach((element) => {
      element.classList.remove("feedback-highlight-selected");
    });
    this.highlightedElements = [];
  }

  updateHighlightStatusActive() {
    const status = document.getElementById("feedbackHighlightStatus");
    if (status) {
      status.innerHTML = `
        <div class="feedback-highlight-status-content">
          <i class="fas fa-highlighter" style="color: #007bff;"></i>
          <span><strong>Click on page content to select the element</strong></span>
        </div>
      `;
      status.classList.add("selected");
    }
  }

  updateHighlightStatusWithSelection() {
    const status = document.getElementById("feedbackHighlightStatus");
    if (status) {
      if (this.highlightedElements.length === 0) {
        status.innerHTML = `
          <div class="feedback-highlight-status-content">
            <i class="fas fa-mouse-pointer"></i>
            <span>Click here to select the relevant text area</span>
          </div>
        `;
        status.classList.remove("selected");
      } else {
        status.innerHTML = `
          <div class="feedback-highlight-status-content">
            <i class="fas fa-check-circle" style="color: #28a745;"></i>
            <span><strong>${this.highlightedElements.length} element(s) selected</strong></span>
            <span style="font-size: 0.75rem; margin-top: 0.25rem;">Click here to change selection</span>
          </div>
        `;
        status.classList.add("selected");
      }
    }
  }

  resetForm() {
    // Clear highlights
    this.clearHighlights();

    // Reset textarea
    const textarea = document.getElementById("feedbackText");
    if (textarea) {
      textarea.value = "";
    }

    // Reset highlight status
    const status = document.getElementById("feedbackHighlightStatus");
    if (status) {
      status.innerHTML = `
        <div class="feedback-highlight-status-content">
          <i class="fas fa-mouse-pointer"></i>
          <span>Click here to select the relevant text area</span>
        </div>
      `;
      status.classList.remove("selected");
      status.classList.add("clickable");
    }
  }

  async submitFeedback() {
    const feedbackText = document.getElementById("feedbackText").value.trim();

    if (!feedbackText) {
      alert("Please enter your feedback before submitting.");
      return;
    }

    // Get highlighted elements info
    const highlightedInfo = this.highlightedElements.map((element) => ({
      tagName: element.tagName,
      text: element.textContent?.substring(0, 100) || "",
      className: element.className,
      id: element.id,
    }));

    let feedbackContent =
      "User gave feedback '" +
      feedbackText +
      "' on element '" +
      highlightedInfo[0].text +
      "' on page '" +
      document.title;

    // Show success message immediately
    this.showFeedbackSubmitted();

    // Send feedback in background (don't await)
    this.sendFeedbackToGoogleCloud(feedbackContent, window.location.href).catch(
      (error) => {
        console.error("Error sending feedback:", error);
        // Could show a subtle error indicator here if needed
      },
    );
  }

  async sendFeedbackToGoogleCloud(feedback, url) {
    // Use the same endpoint as the existing feedback system
    const response = await fetch("https://feedback-43tn7xos3a-uc.a.run.app", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      mode: "cors",
      credentials: "omit",
      body: JSON.stringify({
        value: 2,
        feedback: feedback,
        url: url,
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response;
  }

  showFeedbackSubmitted() {
    const button = document.getElementById("feedbackButtonToc");
    const form = document.getElementById("feedbackForm");

    if (button) {
      button.innerHTML =
        '<span><i class="fas fa-check fa-sm" style="margin-right: 0.5rem; color: #28a745;"></i>Feedback submitted</span>';
      button.classList.remove("feedback-active");
      button.classList.add("feedback-submitted");
    }

    if (form) {
      form.style.display = "none";
    }

    // Reset form state
    this.resetForm();

    // Auto-reset button after 3 seconds
    setTimeout(() => {
      this.resetFeedbackButton();
    }, 3000);
  }

  resetFeedbackButton() {
    const button = document.getElementById("feedbackButtonToc");
    if (button) {
      button.innerHTML =
        '<span><i class="fas fa-comment-dots fa-sm" style="margin-right: 0.5rem"></i>Give Feedback</span>';
      button.classList.remove("feedback-submitted");
    }
  }
}

// Initialize feedback system when DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
  new FeedbackSystem();
});
