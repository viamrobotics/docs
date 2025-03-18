// Inkeep START
const INKEEP_API_KEY = "b17e5b4e252d7ce29b48a48a3dcba6fcfdc045680e8ea576";
const INKEEP_INTEGRATION_ID = "cm3ogfzp4003f29brrf16r6gm";
const INKEEP_ORGANIZATION_ID = "org_yjUXfeVC1tTVMIoY";

// Get the button element
const inkeepButtonTop = document.getElementById("chatButtonTop");
const inkeepButtonBottom = document.getElementById("chatButton");

// Create a new div element to hold the Inkeep modal and set its id and position
const inkeepDiv = document.createElement("div");
inkeepDiv.id = "inkeepModal";
inkeepDiv.style.position = "absolute";

document.body.appendChild(inkeepDiv);

const handleClose = () => {
inkeepWidgetAI.render({
    ...config,
    isOpen: false,
});
};

const handleOpen = () => {
inkeepWidgetAI.render({
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
        defaultView: "AI_CHAT",
        isShortcutKeyEnabled: false,
        isModeSwitchingEnabled: false
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
              "How to install Viam on microcontrollers?",
              "How to deploy a person detection model?",
              "How can I ingest data from machines?",
              "How to query sensor data with third-party tools?",
          ],
      },
  },
};

// Start search elments

// Embed the widget using the `Inkeep.embed()` function.
const inkeepWidgetAI = Inkeep().embed(config);

// Add event listener to open the Inkeep modal when the button is clicked
inkeepButtonTop.addEventListener("click", handleOpen);

// Create an HTML element that the Inkeep widget will be inserted into.
const nav = document.querySelector("#navsearch");
const sidebar = document.getElementById("mobile-search");
const middleNav = document.querySelector("#main_navbar");


const inkeepNavDiv = document.createElement("div");
inkeepNavDiv.id = "navSearchBar";
middleNav.appendChild(inkeepNavDiv);

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
const inkeepWidgetSearch = Inkeep().embed({
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
          isModeSwitchingEnabled: false
      },
      searchSettings: {
        shouldShowAskAICard: false
          // optional settings
      },
      tabSettings: {
        isAllTabEnabled: true,
        rootBreadcrumbsToUseAsTabs: ["Docs", "Blog", "GitHub", "Viam.com"]
      },
    },
});
};

sidebar &&
addInkeepWidget({
  targetElement: document.getElementById("sideSearchBar"),
  stylesheetUrls: ['https://docs.viam.com/css/inkeep.css'],
  isShortcutKeyEnabled: false,
});

addInkeepWidget({
  targetElement: document.getElementById("navSearchBar"),
  stylesheetUrls: ['https://docs.viam.com/css/inkeep.css'],
  isShortcutKeyEnabled: true,
});
