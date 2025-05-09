// Listen for installation
chrome.runtime.onInstalled.addListener(() => {
  console.log('AI Bookmark Manager installed');
});

// Listen for messages from popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'analyzeBookmarks') {
    // Handle bookmark analysis
    chrome.bookmarks.getTree((bookmarkTreeNodes) => {
      sendResponse({ bookmarks: bookmarkTreeNodes });
    });
    return true; // Required for async sendResponse
  }
}); 