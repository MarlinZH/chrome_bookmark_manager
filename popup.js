import OSOMIntegration from './osom-integration.js';
import NotionIntegration from './notion-integration.js';

document.addEventListener('DOMContentLoaded', () => {
  const folderList = document.getElementById('folder-list');
  const recommendationList = document.getElementById('recommendation-list');
  const bookmarkList = document.getElementById('bookmark-list');
  const newFolderNameInput = document.getElementById('new-folder-name');
  const createFolderButton = document.getElementById('create-folder-button');
  const analyzeBtn = document.getElementById('analyzeBtn');
  const loadingDiv = document.querySelector('.loading');
  const categoriesDiv = document.getElementById('categories');
  const organizationDiv = document.getElementById('organization');

  // Notion Integration Elements
  const notionTokenInput = document.getElementById('notion-token');
  const notionDatabaseInput = document.getElementById('notion-database');
  const exportToNotionButton = document.getElementById('export-to-notion');

  const osom = new OSOMIntegration();
  let allBookmarks = [];
  let existingFoldersData = [];

  // Show/hide loading state
  function setLoading(isLoading) {
    loadingDiv.style.display = isLoading ? 'block' : 'none';
    analyzeBtn.disabled = isLoading;
  }

  // Function to display existing folders
  function displayExistingFolders(folders) {
    folderList.innerHTML = '';
    folders.forEach(folder => {
      if (folder.title) {
        const listItem = document.createElement('li');
        listItem.textContent = folder.title;
        listItem.addEventListener('click', () => displayBookmarksInFolder(folder.id));
        folderList.appendChild(listItem);
        existingFoldersData.push({ id: folder.id, title: folder.title });
      }
      if (folder.children) {
        displayExistingFolders(folder.children);
      }
    });
  }

  // Function to display bookmarks in a selected folder
  function displayBookmarksInFolder(folderId) {
    chrome.bookmarks.getChildren(folderId, (bookmarks) => {
      bookmarkList.innerHTML = '';
      bookmarks.forEach(bookmark => {
        if (bookmark.url) {
          const listItem = document.createElement('li');
          const link = document.createElement('a');
          link.href = bookmark.url;
          link.textContent = bookmark.title || bookmark.url;
          link.target = '_blank';
          listItem.appendChild(link);
          bookmarkList.appendChild(listItem);
        }
      });
    });
  }

  // Function to display recommended folders
  function displayRecommendedFolders(recommendations) {
    recommendationList.innerHTML = '';
    recommendations.forEach(recommendation => {
      const listItem = document.createElement('li');
      listItem.textContent = `${recommendation.category} (${recommendation.score})`;
      listItem.addEventListener('click', () => {
        newFolderNameInput.value = recommendation.category;
      });
      recommendationList.appendChild(listItem);
    });
  }

  // Function to get all bookmarks
  async function getAllBookmarks() {
    return new Promise((resolve) => {
      chrome.bookmarks.getTree(results => {
        function flattenBookmarks(nodes) {
          nodes.forEach(node => {
            if (node.url) {
              allBookmarks.push(node);
            }
            if (node.children) {
              flattenBookmarks(node.children);
            }
          });
        }
        flattenBookmarks(results);
        resolve(allBookmarks);
      });
    });
  }

  // Analyze bookmarks using OSOM
  async function analyzeBookmarks(bookmarks) {
    const categoryScores = new Map();
    
    for (const bookmark of bookmarks) {
      const analysis = await osom.analyzeContent(bookmark.url, bookmark.title);
      const topCategories = osom.getTopCategories(analysis);
      
      topCategories.forEach(({ category, score }) => {
        const currentScore = categoryScores.get(category) || 0;
        categoryScores.set(category, currentScore + score);
      });
    }
    
    // Convert to array and sort by score
    return Array.from(categoryScores.entries())
      .map(([category, score]) => ({
        category,
        score: Math.round((score / bookmarks.length) * 100) / 100
      }))
      .sort((a, b) => b.score - a.score)
      .slice(0, 5);
  }

  // Display results
  function displayResults(categories) {
    categoriesDiv.innerHTML = categories
      .map(({ category, score }) => `
        <div class="flex justify-between items-center p-2 bg-gray-50 rounded">
          <span class="text-gray-700">${category}</span>
          <span class="text-sm text-gray-500">Score: ${score}</span>
        </div>
      `)
      .join('');
  }

  // Main analysis function
  async function analyze() {
    try {
      setLoading(true);
      
      // Get bookmarks
      const bookmarks = await getAllBookmarks();
      
      // Analyze bookmarks
      const categories = await analyzeBookmarks(bookmarks);
      
      // Display results
      displayResults(categories);
      displayRecommendedFolders(categories);
      
    } catch (error) {
      console.error('Error:', error);
      alert('An error occurred while analyzing bookmarks.');
    } finally {
      setLoading(false);
    }
  }

  // Event listener for creating a new folder
  createFolderButton.addEventListener('click', () => {
    const newFolderName = newFolderNameInput.value.trim();
    if (newFolderName) {
      chrome.bookmarks.create({ title: newFolderName }, (newFolder) => {
        newFolderNameInput.value = '';
        // Re-fetch and re-display folders to show the new one
        chrome.bookmarks.getTree(results => {
          const topLevelFolders = results[0].children.filter(node => !node.url);
          displayExistingFolders(topLevelFolders);
        });
      });
    }
  });

  // Event listeners
  analyzeBtn.addEventListener('click', analyze);

  // Initial load
  chrome.bookmarks.getTree(results => {
    const topLevelFolders = results[0].children.filter(node => !node.url);
    displayExistingFolders(topLevelFolders);
    getAllBookmarks(); // This will trigger the AI analysis and recommendation display
  });

  // Load saved Notion credentials
  chrome.storage.local.get(['notionToken', 'notionDatabaseId'], (result) => {
    if (result.notionToken) notionTokenInput.value = result.notionToken;
    if (result.notionDatabaseId) notionDatabaseInput.value = result.notionDatabaseId;
  });

  // Save Notion credentials when changed
  notionTokenInput.addEventListener('change', () => {
    chrome.storage.local.set({ notionToken: notionTokenInput.value });
  });

  notionDatabaseInput.addEventListener('change', () => {
    chrome.storage.local.set({ notionDatabaseId: notionDatabaseInput.value });
  });

  // Export to Notion functionality
  exportToNotionButton.addEventListener('click', async () => {
    const token = notionTokenInput.value.trim();
    const databaseId = notionDatabaseInput.value.trim();

    if (!token || !databaseId) {
      alert('Please enter both Notion token and database ID');
      return;
    }

    try {
      setLoading(true);
      const notion = new NotionIntegration(token, databaseId);
      
      // Get all bookmarks with their folder structure
      const bookmarks = await getAllBookmarksWithFolders();
      
      // Export to Notion
      const results = await notion.importBookmarks(bookmarks);
      
      // Show results
      const successCount = results.filter(r => r.success).length;
      const failCount = results.length - successCount;
      
      alert(`Export completed!\nSuccessfully exported: ${successCount}\nFailed: ${failCount}`);
      
    } catch (error) {
      console.error('Error exporting to Notion:', error);
      alert('Error exporting to Notion: ' + error.message);
    } finally {
      setLoading(false);
    }
  });

  // Function to get all bookmarks with their folder structure
  async function getAllBookmarksWithFolders() {
    return new Promise((resolve) => {
      chrome.bookmarks.getTree(results => {
        const bookmarks = [];
        
        function processNode(node, currentPath = '') {
          if (node.url) {
            bookmarks.push({
              title: node.title,
              url: node.url,
              folder: currentPath
            });
          }
          
          if (node.children) {
            const newPath = currentPath ? `${currentPath}/${node.title}` : node.title;
            node.children.forEach(child => processNode(child, newPath));
          }
        }
        
        processNode(results[0]);
        resolve(bookmarks);
      });
    });
  }
}); 