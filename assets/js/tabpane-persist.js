// Utilities
const _tdStoragePersistKey = (tabKey) => "td-tp-persist:" + (tabKey || "");

const _tdSupportsLocalStorage = () => typeof Storage !== "undefined";

// Check if Cookiebot is available and user has consented
const _tdHasCookieConsent = () => {
  // If Cookiebot is not loaded, assume consent (for backwards compatibility)
  if (typeof Cookiebot === "undefined") {
    return true;
  }

  // Check if user has consented to preferences or necessary cookies
  // localStorage for tab preferences typically falls under "preferences" category
  return Cookiebot.consent.preferences || Cookiebot.consent.necessary;
};

// Helpers
function tdPersistKey(key, value) {
  // @requires: tdSupportsLocalStorage();
  if (!_tdHasCookieConsent()) {
    // Silently fail if no consent - don't store anything
    return;
  }

  try {
    if (value) {
      localStorage.setItem(key, value);
    } else {
      localStorage.removeItem(key);
    }
  } catch (error) {
    const action = value ? "add" : "remove";
    console.error(
      `Docsy tabpane: unable to ${action} localStorage key '${key}': `,
      error,
    );
  }
}

// Retrieve, increment, and store tab-select event count, then returns it.
function tdGetTabSelectEventCountAndInc() {
  // @requires: tdSupportsLocalStorage();
  if (!_tdHasCookieConsent()) {
    return 0; // Return 0 if no consent
  }

  const storedCount = localStorage.getItem("td-tp-persist-count");
  let numTabSelectEvents = parseInt(storedCount) || 0;
  numTabSelectEvents++;
  tdPersistKey("td-tp-persist-count", numTabSelectEvents.toString());
  return numTabSelectEvents;
}

// Main functions

function tdActivateTabsWithKey(key, clicked_element, rectangle) {
  if (!key) return;

  document
    .querySelectorAll(`.nav-tabs > .nav-item > a[data-td-tp-persist='${key}']`)
    .forEach((element) => {
      if (element == clicked_element) {
        // Ensures that if the dom changes above the element, the user's view
        // doesn't jump
        window.scrollBy(0, element.getBoundingClientRect().top - rectangle.top);
      }
      new bootstrap.Tab(element).show();
    });
}

function tdPersistActiveTab(activeTabKey) {
  if (!_tdSupportsLocalStorage()) return;

  tdPersistKey(
    _tdStoragePersistKey(activeTabKey),
    tdGetTabSelectEventCountAndInc(),
  );
}

// Handlers

function tdGetAndActivatePersistedTabs(tabs) {
  // Only switch tabs for programming languages, web ui, and cli
  var keyOfTabsInThisPage = [
    "Web UI",
    "CLI",
    "Python",
    "Go",
    "C++",
    "TypeScript",
    "Flutter",
    "Python: venv",
    "Python: Hot reloading (recommended)",
    "Python: PyInstaller (recommended)",
  ];

  // Don't try to read from localStorage if no consent
  if (!_tdHasCookieConsent()) {
    return [];
  }

  // Create a list of active tabs with their age:
  let key_ageList = keyOfTabsInThisPage
    // Map to [tab-key, last-activated-age]
    .map((k) => [
      k,
      parseInt(localStorage.getItem(_tdStoragePersistKey(k))) || 0,
    ])
    // Exclude tabs that have never been activated
    .filter(([k, v]) => v)
    // Sort from oldest selected to most recently selected
    .sort((a, b) => a[1] - b[1]);

  // Activate tabs from the oldest to the newest
  key_ageList.forEach(([key]) => {
    tdActivateTabsWithKey(key);
  });

  return key_ageList;
}

function tdRegisterTabClickHandler(tabs) {
  tabs.forEach((tab) => {
    if (
      [
        "Web UI",
        "CLI",
        "Python",
        "Go",
        "C++",
        "TypeScript",
        "Flutter",
        "Python: venv",
        "Python: Hot reloading (recommended)",
        "Python: PyInstaller (recommended)",
      ].includes(tab.text)
    ) {
      tab.addEventListener("click", (event) => {
        const activeTabKey = tab.getAttribute("data-td-tp-persist");
        tdPersistActiveTab(activeTabKey);
        tdActivateTabsWithKey(
          activeTabKey,
          event.srcElement,
          event.srcElement.getBoundingClientRect(),
        );
      });
    } else {
      tab.addEventListener("click", (event) => {
        const activeTabKey = tab.getAttribute("data-td-tp-persist");
        tdActivateTabsWithKey(
          activeTabKey,
          event.srcElement,
          event.srcElement.getBoundingClientRect(),
        );
      });
    }
  });
}

// Register listeners and activate tabs
window.addEventListener("DOMContentLoaded", () => {
  if (!_tdSupportsLocalStorage()) return;

  // Wait for Cookiebot to be ready if it's available
  const initializeTabPersistence = () => {
    var allTabsInThisPage = document.querySelectorAll(
      ".nav-tabs > .nav-item > a",
    );
    tdRegisterTabClickHandler(allTabsInThisPage);
    if (document.getElementsByTagName("h1").length) {
      if (document.getElementsByTagName("h1")[0].textContent != "Dev tools") {
        tdGetAndActivatePersistedTabs(allTabsInThisPage);
      }
    }
  };

  // If Cookiebot is available, wait for consent to be determined
  if (typeof Cookiebot !== "undefined") {
    // Listen for Cookiebot consent update events
    window.addEventListener(
      "CookiebotOnConsentReady",
      initializeTabPersistence,
    );
    window.addEventListener("CookiebotOnAccept", initializeTabPersistence);

    // Also try immediately in case consent was already given
    if (Cookiebot.consent.preferences || Cookiebot.consent.necessary) {
      initializeTabPersistence();
    }
  } else {
    // If Cookiebot is not available, initialize immediately (backwards compatibility)
    initializeTabPersistence();
  }

  // Open Anchor for expanders if hidden START
  const openDetailsIfAnchorHidden = (evt) => {
    const target = evt.currentTarget.getAttribute("href"); // "#anchored"

    // Validate that the href is a valid selector (starts with # and has content after it)
    if (!target || target === "#" || !target.startsWith("#")) {
      return; // Invalid or empty href, do nothing
    }

    const elTarget = document.querySelector(target);

    if (!elTarget) return; // No such element in DOM. Do nothing

    // Open all <details> ancestors
    let elDetails = elTarget.closest("details");

    while (elDetails) {
      if (elDetails.matches("details")) elDetails.open = true;
      elDetails = elDetails.parentElement;
    }
  };

  document.querySelectorAll("[href^='#']").forEach((el) => {
    el.addEventListener("click", openDetailsIfAnchorHidden);
  });

  document.addEventListener("DOMContentLoaded", function (event) {
    if (location.hash) {
      hash = document.getElementById(location.hash.substr(1));
      details = hash.closest("details");
      if (details) {
        bbox = details.getBoundingClientRect();
        scrollTo(bbox.x, bbox.y - 120);
      }
    }
  });

  // Open Anchor for expanders if hidden END
});
