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