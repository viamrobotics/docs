// script for menu toggles
var siteMenuSubmenus = document.getElementsByClassName(
    "nav-fold"
);

function submenuToggle(menu, toggle) {
    let open = false;
    if (toggle.children[0].className === "fas fa-chevron-right") {
        open = true;
    }

    // toggle displayed icon
    if (open) {
        toggle.children[0].className = "fas fa-chevron-down";
    } else {
        toggle.children[0].className = "fas fa-chevron-right";
    }

    // add or remove collapse class to children
    let immediateChildren = menu.querySelector("ul").children;
    if (open) {
        for (let c of immediateChildren) {
            c.classList.remove("collapse");
        }
    } else {
        for (let c of immediateChildren) {
            c.classList.add("collapse");
        }
    }
}

for (let menu of siteMenuSubmenus) {
    // add event listener on menu toggle
    let toggle = menu.querySelector("span").querySelector(".menu-toggle");
    if (toggle) {
        if (menu.classList.contains('empty-node-submenu')) {
            menu.querySelector(".emptynode").addEventListener('click', function () {
                submenuToggle(menu, toggle);
            });
        }
        toggle.addEventListener('click', function () {
            submenuToggle(menu, toggle);
        });
    }
};

// script for the scroll button
const main = document.body;
const scrollBtn = document.getElementById("scrollButton");
function toTop() {
    window.scroll({top: 0, left: 0, behavior: 'smooth'});
}

function btnVisibility(payload) {
    if (payload[0].boundingClientRect.y <= -400) {
        scrollBtn.style.visibility = "visible";
        scrollBtn.style.opacity = "1";
    } else {
        scrollBtn.style.opacity = "0";
        scrollBtn.style.visibility = "hidden";
    }
}

if(main && scrollBtn) {
    const observer = new IntersectionObserver(btnVisibility, {
        threshold: [0, 0.2, 0.4, 0.6, 0.8, 1.0]
    });
    observer.observe(main);
}

// Inkeep START

const INKEEP_API_KEY = "b17e5b4e252d7ce29b48a48a3dcba6fcfdc045680e8ea576";
const INKEEP_INTEGRATION_ID = "cm3ogfzp4003f29brrf16r6gm";
const INKEEP_ORGANIZATION_ID = "org_yjUXfeVC1tTVMIoY";

// Get the button element
const inkeepButton = document.getElementById("chatButton");

// Create a new div element to hold the Inkeep modal and set its id and position
const inkeepDiv = document.createElement("div");
inkeepDiv.id = "inkeepModal";
inkeepDiv.style.position = "absolute";
document.body.appendChild(inkeepDiv);

const handleClose = () => {
inkeepWidget.render({
    ...config,
    isOpen: false,
});
};

const handleOpen = () => {
inkeepWidget.render({
    ...config,
    isOpen: true,
});
}

const config = {
componentType: "CustomTrigger", // required
targetElement: inkeepDiv, // required
properties: {
    isOpen: false, // required
    onClose: handleClose, // required
    onOpen: undefined,
    baseSettings: {
    apiKey: INKEEP_API_KEY,
    integrationId: INKEEP_INTEGRATION_ID,
    organizationId: INKEEP_ORGANIZATION_ID,
    primaryBrandColor: "#000000",
    organizationDisplayName: "Viam AI Bot",
    //... optional base settings
    },
    modalSettings: {
    // optional InkeepModalSettings
    },
    searchSettings: {
    // optional InkeepSearchSettings
    },
    aiChatSettings: {
        chatSubjectName: "Viam",
        botAvatarSrcUrl: "https://cdn.prod.website-files.com/62fba5686b6d47fe2a1ed2a6/62fba8f4a8ca05f38a2b497f_viam-logo-webclip.png",
        botAvatarDarkSrcUrl: "https://storage.googleapis.com/organization-image-assets/viam-botAvatarDarkSrcUrl-1721328398594.svg",
        getHelpCallToActions: [
            {
                name: "Email",
                url: "mailto:support@viam.com",
                icon: {
                    builtIn: "IoMail"
                }
            },
            {
                name: "Discord",
                url: "https://discord.gg/viam",
                icon: {
                    builtIn: "FaDiscord"
                }
            }
        ],
        quickQuestions: [
            "How to install lightweight version microcontroller?",
            "How to deploy a person detection model?",
            "How can I ingest data from machines?",
            "How to query sensor data with third-party tools?",
        ],
    },
},
};

// Embed the widget using the `Inkeep.embed()` function.
const inkeepWidget = Inkeep().embed(config);

// Add event listener to open the Inkeep modal when the button is clicked
inkeepButton.addEventListener("click", handleOpen);

// Create an HTML element that the Inkeep widget will be inserted into.
const nav = document.querySelector("nav");
const sidebar = document.getElementById("mobile-search");

const inkeepNavDiv = document.createElement("div");
inkeepNavDiv.id = "navSearchBar";
nav.appendChild(inkeepNavDiv);

const inkeepSidebarDiv = document.createElement("div");
inkeepSidebarDiv.id = "sideSearchBar";
sidebar && sidebar.prepend(inkeepSidebarDiv);

// Function for initializating the widget.
const addInkeepWidget = ({
  targetElement,
  stylesheetUrls,
  isShortcutKeyEnabled,
}) => {
  // Embed the widget using the `Inkeep.embed()` function.
  const inkeepWidget = Inkeep().embed({
    componentType: "SearchBar",
    targetElement,
    properties: {
      baseSettings: {
        apiKey: INKEEP_API_KEY,
        integrationId: INKEEP_INTEGRATION_ID,
        organizationId: INKEEP_ORGANIZATION_ID,
        primaryBrandColor: "#000000", // your brand color, widget color scheme is derived from this
        organizationDisplayName: "Viam AI Bot",
        // ...optional settings
        theme: {
          stylesheetUrls,
          // ...optional settings
        },
      },
      modalSettings: {
        // optional settings
        isShortcutKeyEnabled,
      },
      searchSettings: {
        // optional settings
      },
      aiChatSettings: {
        chatSubjectName: "Viam",
        botAvatarSrcUrl: "https://cdn.prod.website-files.com/62fba5686b6d47fe2a1ed2a6/62fba8f4a8ca05f38a2b497f_viam-logo-webclip.png",
        botAvatarDarkSrcUrl: "https://storage.googleapis.com/organization-image-assets/viam-botAvatarDarkSrcUrl-1721328398594.svg",
        getHelpCallToActions: [
            {
                name: "Email",
                url: "mailto:support@viam.com",
                icon: {
                    builtIn: "IoMail"
                }
            },
            {
                name: "Discord",
                url: "https://discord.gg/viam",
                icon: {
                    builtIn: "FaDiscord"
                }
            }
        ],
        quickQuestions: [
            "How to install lightweight version microcontroller?",
            "How to deploy a person detection model?",
            "How can I ingest data from machines?",
            "How to query sensor data with third-party tools?",
        ],
      },
    },
  });
};

sidebar &&
  addInkeepWidget({
    targetElement: document.getElementById("sideSearchBar"),
    // stylesheetUrls: ['/path/to/stylesheets'], // optional
    isShortcutKeyEnabled: false,
  });

addInkeepWidget({
  targetElement: document.getElementById("navSearchBar"),
//   stylesheetUrls: ['/path/to/stylesheets'], // optional
  isShortcutKeyEnabled: true,
});

// Inkeep END