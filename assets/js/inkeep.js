// Inkeep START
const INKEEP_API_KEY = "b17e5b4e252d7ce29b48a48a3dcba6fcfdc045680e8ea576";
const INKEEP_INTEGRATION_ID = "cm3ogfzp4003f29brrf16r6gm";
const INKEEP_ORGANIZATION_ID = "org_yjUXfeVC1tTVMIoY";

// Get the button element
const inkeepButtonBottom = document.getElementById("chatButton");

// Create a new div element to hold the Inkeep modal and set its id and position
const inkeepDiv = document.createElement("div");
inkeepDiv.id = "inkeepModal";
inkeepDiv.style.position = "absolute";

document.body.appendChild(inkeepDiv);

function handleOpenChange(newOpen) {
  inkeepWidgetAI.update({ modalSettings: { isOpen: newOpen } });
}

let searchBarWidget;

const config = {
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
        onOpenChange: handleOpenChange,
      },
      aiChatSettings: {
          aiAssistantName: "Viam",
          chatSubjectName: "Viam",
          aiAssistantAvatar: "https://cdn.prod.website-files.com/62fba5686b6d47fe2a1ed2a6/62fba8f4a8ca05f38a2b497f_viam-logo-webclip.png",
          userAvatarSrcUrl: "https://storage.googleapis.com/organization-image-assets/viam-botAvatarDarkSrcUrl-1721328398594.svg",
          introMessage: "Hi!\n\nI'm an AI assistant trained on documentation, help articles, and other content. \n\nHow can I help you today?\n\n_Please do not share sensitive information such as secrets or API keys with me._",
          getHelpOptions: [
            {
              icon: { builtIn: "IoMail" },
              name: "Email",
              action: {
                type: "open_link",
                url: "mailto:support@viam.com",
              },
            },
            {
              icon: { builtIn: "FaDiscord" },
              name: "Discord",
              action: {
                type: "open_link",
                url: "https://discord.gg/viam",
              },
            },
          ],
          exampleQuestions: [
              "How do I install Viam on a single-board computer?",
              "How do I deploy a person detection model?",
              "How to ingest data from machines",
              "How can I query sensor data with third-party tools?",
          ],
      },
      canToggleView: false,
};

// Start search elments

// Embed the widget using the `Inkeep.embed()` function.
const inkeepWidgetAI = Inkeep.ModalChat(config);

// Add event listener to open the Inkeep modal when the button is clicked
inkeepButtonBottom.addEventListener("click",  () => {
  inkeepWidgetAI.update({ modalSettings: { isOpen: true } });
});

// Initialize the Ask AI dropdown functionality
function initializeAskAIDropdown(searchBarWidget) {
  const askAiButton = document.getElementById('askAiButtonToc');
  const aiDropdownMenu = document.getElementById('aiDropdownMenuToc');

  if (askAiButton && aiDropdownMenu) {
    // Toggle dropdown when button is clicked
    askAiButton.addEventListener('click', function(e) {
      e.stopPropagation();
      aiDropdownMenu.classList.toggle('show');
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', function(e) {
      if (!askAiButton.contains(e.target) && !aiDropdownMenu.contains(e.target)) {
        aiDropdownMenu.classList.remove('show');
      }
    });

    // Handle AI service clicks
    aiDropdownMenu.addEventListener('click', function(e) {
      const aiItem = e.target.closest('.ai-dropdown-item-toc');
      if (aiItem) {
        e.preventDefault();

        const aiService = aiItem.getAttribute('data-ai-service');
        const action = aiItem.getAttribute('data-action');
        const pageUrl = aiItem.getAttribute('data-page-url');
        const pageTitle = aiItem.getAttribute('data-page-title');

        if (action === 'use-mcp') {
          // Open the Inkeep MCP URL directly
          window.open('https://share.inkeep.com/viam/mcp', '_blank');
        } else if (aiService === 'inkeep') {
          // Open the Inkeep widget modal and switch to chat view
          searchBarWidget.setView("chat");
          searchBarWidget.update({
            modalSettings: {
              isOpen: true,
              onOpenChange: (isOpen) => {
                if (!isOpen) {
                  // When closing, reset to search view
                  searchBarWidget.setView("search");
                  searchBarWidget.update({
                    modalSettings: {
                      isOpen: false,
                    }
                  });
                } else {
                  searchBarWidget.update({
                    modalSettings: {
                      isOpen: true,
                    }
                  });
                }
              }
            }
          });
        } else if (aiService && pageUrl && pageTitle) {
          openAIService(aiService, pageUrl, pageTitle);
        }

        // Close dropdown
        aiDropdownMenu.classList.remove('show');
      }
    });
  }
}

function openAIService(service, pageUrl, pageTitle) {
  const prompt = `Hi! Can you please read [this page](${pageUrl}) and prepare to answer questions about it?`;

  let serviceUrl = '';
  switch (service) {
    case 'claude':
      serviceUrl = `https://claude.ai/new?q=${prompt}`;
      break;
    case 'chatgpt':
      serviceUrl = `https://chatgpt.com/?hints=search&prompt=${prompt}`;
      break;
    case 'copilot':
      serviceUrl = `https://copilot.microsoft.com/?q=${prompt}`;
      break;
  }

  if (serviceUrl) {
    // Open the AI service in a new tab
    const newTab = window.open(serviceUrl, '_blank');

    // Wait a moment for the tab to open, then try to paste the prompt
    setTimeout(() => {
      try {
        newTab.focus();
      } catch (e) {
        // Cross-origin restrictions might prevent this
        console.log('Could not focus new tab due to cross-origin restrictions');
      }
    }, 100);
  }
}

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

  const config = {
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
      transformSource: (source, type, opts) => {
        let tabs = [ "Docs" ];
        let openInNewTab = true;
        if (source.type === "github_issue") {
          tabs = [ "GitHub" ];
        } else {
          if (source.url.includes("https://www.viam.com")) {
            if (source.url.includes("https://www.viam.com/post")) {
              tabs = [ "Blog" ];
            } else {
              tabs = [ "viam.com" ];
            }
          } else if (source.url.includes("https://codelabs.viam.com")) {
            tabs = [ "Codelab" ];
          } else if (source.url.includes("https://app.viam.com/")) {
            tabs = [ "Modules" ];
          } else if (source.url.includes("https://github.com/")) {
            tabs = [ "GitHub" ];
          } else if (source.url.includes("https://python.viam.dev/") | source.url.includes("https://pkg.go.dev/") | source.url.includes("https://flutter.viam.dev/") | source.url.includes("https://cpp.viam.dev/") | source.url.includes("https://ts.viam.dev/") ) {
            tabs = [ "SDK Docs" ];
          } else if (source.url.includes("https://docs.viam.com/tutorials/")) {
            tabs = [ "Tutorials" ];
          } else {
            tabs = [ "Docs" ];
            openInNewTab = false;
          }
        }

        // Transform based on source type
        if (type === "searchResultItem") {
          return {
            ...source,
            title: `${source.title}`,
            description: source.description?.slice(0, 150) + "...",
            breadcrumbs: [...(source.breadcrumbs || [])],
            tabs: tabs,
            //  [
              // "API",
              // [
              //   "Docs", { breadcrumbs: ["Forums", "Reference"] }
              // ]
            // ],
            shouldOpenInNewTab: openInNewTab,
            appendToUrl: { source: type },
          };
        }

        return source;
      },
    },
    aiChatSettings: {
      aiAssistantName: "Viam",
      chatSubjectName: "Viam",
      aiAssistantAvatar: "https://cdn.prod.website-files.com/62fba5686b6d47fe2a1ed2a6/62fba8f4a8ca05f38a2b497f_viam-logo-webclip.png",
      userAvatarSrcUrl: "https://storage.googleapis.com/organization-image-assets/viam-botAvatarDarkSrcUrl-1721328398594.svg",
      introMessage: "Hi!\n\nI'm an AI assistant trained on documentation, help articles, and other content. \n\nHow can I help you today?\n\n_Please do not share sensitive information such as secrets or API keys with me._",
      getHelpOptions: [
        {
          icon: { builtIn: "IoMail" },
          name: "Email",
          action: {
            type: "open_link",
            url: "mailto:support@viam.com",
          },
        },
        {
          icon: { builtIn: "FaDiscord" },
          name: "Discord",
          action: {
            type: "open_link",
            url: "https://discord.gg/viam",
          },
        },
      ],
      exampleQuestions: [
          "How do I install Viam on a single-board computer?",
          "How do I deploy a person detection model?",
          "How to ingest data from machines",
          "How can I query sensor data with third-party tools?",
      ],
    },
    canToggleView: true,
    searchSettings: {
      placeholder: "Search or ask AI...",
      tabs: [
        "All",
        ["Docs", { isAlwaysVisible: true }],
        "Modules",
        "SDK Docs",
        "GitHub",
        "Tutorials",
        "Codelab",
        "Blog",
        "viam.com",
      ],
    },
  };

  // Initialize the widget
  searchBarWidget = Inkeep.SearchBar(targetElement, config);

};

sidebar &&
addInkeepWidget({
  targetElement: "#sideSearchBar",
  stylesheetUrls: ['https://docs.viam.com/css/inkeep.css'],
  isShortcutKeyEnabled: false,
});

addInkeepWidget({
  targetElement: "#navSearchBar",
  stylesheetUrls: ['https://docs.viam.com/css/inkeep.css'],
  isShortcutKeyEnabled: true,
});

// Initialize the Ask AI dropdown after the page is loaded
document.addEventListener('DOMContentLoaded', function() {
  initializeAskAIDropdown(searchBarWidget);
});
