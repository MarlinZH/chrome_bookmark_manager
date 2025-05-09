document.addEventListener('DOMContentLoaded', () => {
  const folderList = document.getElementById('folder-list');
  const recommendationList = document.getElementById('recommendation-list');
  const bookmarkList = document.getElementById('bookmark-list');
  const newFolderNameInput = document.getElementById('new-folder-name');
  const createFolderButton = document.getElementById('create-folder-button');

  let allBookmarks = [];
  let existingFoldersData = [];

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
      listItem.textContent = recommendation;
      listItem.addEventListener('click', () => {
        newFolderNameInput.value = recommendation;
      });
      recommendationList.appendChild(listItem);
    });
  }

  // Function to get all bookmarks
  function getAllBookmarks() {
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
      // After fetching bookmarks, trigger AI analysis
      const recommendations = analyzeBookmarks(allBookmarks);
      displayRecommendedFolders(recommendations);
    });
  }

  // Basic keyword-based AI for recommending folders
  function analyzeBookmarks(bookmarks) {
    const keywords = {};
    bookmarks.forEach(bookmark => {
      const title = bookmark.title ? bookmark.title.toLowerCase() : '';
      const urlParts = bookmark.url ? bookmark.url.toLowerCase().split('/').slice(2) : []; // Extract domain and path

      const textToAnalyze = `${title} ${urlParts.join(' ')}`;
      const words = textToAnalyze.split(/\s+/).filter(word => word.length > 2 && !['the', 'a', 'of', 'in', 'com', 'org', 'net', 'www', 'https', 'http'].includes(word));

      words.forEach(word => {
        keywords[word] = (keywords[word] || 0) + 1;
      });
    });

    // Sort keywords by frequency and take top few
    const sortedKeywords = Object.entries(keywords)
      .sort(([, countA], [, countB]) => countB - countA)
      .slice(0, 5)
      .map(entry => entry[0]);

    // Suggest folders based on these keywords
    return sortedKeywords.map(keyword => keyword.charAt(0).toUpperCase() + keyword.slice(1));
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

  // Initial load: get and display existing folders and recommendations
  chrome.bookmarks.getTree(results => {
    const topLevelFolders = results[0].children.filter(node => !node.url);
    displayExistingFolders(topLevelFolders);
    getAllBookmarks(); // This will trigger the AI analysis and recommendation display
  });
});
// DOM Elements
const analyzeBtn = document.getElementById('analyzeBtn');
const loadingDiv = document.querySelector('.loading');
const categoriesDiv = document.getElementById('categories');
const organizationDiv = document.getElementById('organization');

// Show/hide loading state
function setLoading(isLoading) {
  loadingDiv.style.display = isLoading ? 'block' : 'none';
  analyzeBtn.disabled = isLoading;
}

// Fetch bookmarks from Chrome API
async function getBookmarks() {
  return new Promise((resolve) => {
    chrome.bookmarks.getTree((bookmarkTreeNodes) => {
      resolve(bookmarkTreeNodes);
    });
  });
}

// Extract all bookmarks from the tree
function extractBookmarks(bookmarkTreeNodes) {
  const bookmarks = [];
  
  function traverse(nodes) {
    for (const node of nodes) {
      if (node.url) {
        bookmarks.push({
          title: node.title,
          url: node.url
        });
      }
      if (node.children) {
        traverse(node.children);
      }
    }
  }
  
  traverse(bookmarkTreeNodes);
  return bookmarks;
}

// Analyze bookmarks using AI
async function analyzeBookmarks(bookmarks) {
  // Here we'll use a simple keyword extraction for now
  // In a real implementation, you would call an AI API
  const categories = new Map();
  
  bookmarks.forEach(bookmark => {
    const words = bookmark.title.toLowerCase().split(/\s+/);
    words.forEach(word => {
      if (word.length > 3) { // Ignore short words
        categories.set(word, (categories.get(word) || 0) + 1);
      }
    });
  });
  
  return Array.from(categories.entries())
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10)
    .map(([category, count]) => ({ category, count }));
}

// Display results
function displayResults(categories) {
  categoriesDiv.innerHTML = categories
    .map(({ category, count }) => `
      <div class="flex justify-between items-center p-2 bg-gray-50 rounded">
        <span class="text-gray-700">${category}</span>
        <span class="text-sm text-gray-500">${count} bookmarks</span>
      </div>
    `)
    .join('');
}

// Main function
async function analyze() {
  try {
    setLoading(true);
    
    // Get bookmarks
    const bookmarkTree = await getBookmarks();
    const bookmarks = extractBookmarks(bookmarkTree);
    
    // Analyze bookmarks
    const categories = await analyzeBookmarks(bookmarks);
    
    // Display results
    displayResults(categories);
    
  } catch (error) {
    console.error('Error:', error);
    alert('An error occurred while analyzing bookmarks.');
  } finally {
    setLoading(false);
  }
}

// Event listeners
analyzeBtn.addEventListener('click', analyze); 