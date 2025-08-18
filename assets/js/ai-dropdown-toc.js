document.addEventListener('DOMContentLoaded', function() {
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
        } else if (aiService && pageUrl && pageTitle) {
          openAIService(aiService, pageUrl, pageTitle);
        }

        // Close dropdown
        aiDropdownMenu.classList.remove('show');
      }
    });
  }
});

function openAIService(service, pageUrl, pageTitle) {
  const prompt = `Hi! Can you please read [this page](${pageUrl}) and prepare to answer questions about it?`;

  let serviceUrl = '';
  switch (service) {
    case 'claude':
      serviceUrl = 'https://claude.ai';
      break;
    case 'chatgpt':
      serviceUrl = 'https://chat.openai.com';
      break;
    case 'copilot':
      serviceUrl = 'https://copilot.microsoft.com';
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
