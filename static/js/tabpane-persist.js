// Utilities
const _tdStoragePersistKey = (tabKey) =>
   'td-tp-persist:' + (tabKey || '');

const _tdSupportsLocalStorage = () => typeof Storage !== 'undefined';

// Helpers
function tdPersistKey(key, value) {
  // @requires: tdSupportsLocalStorage();
  try {
    if (value) {
      localStorage.setItem(key, value);
    } else {
      localStorage.removeItem(key);
    }
  } catch (error) {
    const action = value ? 'add' : 'remove';
    console.error(
      `Docsy tabpane: unable to ${action} localStorage key '${key}': `,
      error
    );
  }
}

// Retrieve, increment, and store tab-select event count, then returns it.
function tdGetTabSelectEventCountAndInc() {
  // @requires: tdSupportsLocalStorage();

  const storedCount = localStorage.getItem('td-tp-persist-count');
  let numTabSelectEvents = parseInt(storedCount) || 0;
  numTabSelectEvents++;
  tdPersistKey('td-tp-persist-count', numTabSelectEvents.toString());
  return numTabSelectEvents;
}

// Main functions

function tdActivateTabsWithKey(key, clicked_element, rectangle) {
  if (!key) return;

    document.querySelectorAll(`.nav-tabs > .nav-item > a[data-td-tp-persist='${key}']`).forEach((element) => {
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
    tdGetTabSelectEventCountAndInc()
  );
}

// Handlers

function tdGetAndActivatePersistedTabs(tabs) {
  // Get unique persistence keys of tabs in this page
  var keyOfTabsInThisPage = [
    ...new Set(
      Array.from(tabs).map((el) => el.getAttribute("data-td-tp-persist"))
    ),
  ];

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
    tab.addEventListener('click', (event) => {
      const activeTabKey = tab.getAttribute("data-td-tp-persist");
      tdPersistActiveTab(activeTabKey);
      tdActivateTabsWithKey(activeTabKey, event.srcElement, event.srcElement.getBoundingClientRect())
    });
  });
}

// Register listeners and activate tabs
window.addEventListener('DOMContentLoaded', () => {
  if (!_tdSupportsLocalStorage()) return;

  var allTabsInThisPage = document.querySelectorAll(".nav-tabs > .nav-item > a");
  tdRegisterTabClickHandler(allTabsInThisPage);
  tdGetAndActivatePersistedTabs(allTabsInThisPage);
});