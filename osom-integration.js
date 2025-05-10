// OSOM Integration Module
class OSOMIntegration {
  constructor() {
    this.categories = new Map();
    this.weights = new Map();
    this.initializeWeights();
  }

  // Initialize default category weights
  initializeWeights() {
    this.weights.set('technology', 1.2);
    this.weights.set('business', 1.1);
    this.weights.set('education', 1.0);
    this.weights.set('entertainment', 0.9);
    this.weights.set('news', 1.0);
    this.weights.set('social', 0.8);
    this.weights.set('shopping', 0.7);
    this.weights.set('health', 1.1);
    this.weights.set('finance', 1.0);
    this.weights.set('travel', 0.9);
  }

  // Analyze URL and title for categorization
  async analyzeContent(url, title) {
    const urlAnalysis = this.analyzeUrl(url);
    const titleAnalysis = this.analyzeTitle(title);
    
    return this.combineAnalysis(urlAnalysis, titleAnalysis);
  }

  // Analyze URL structure
  analyzeUrl(url) {
    const urlObj = new URL(url);
    const domain = urlObj.hostname;
    const path = urlObj.pathname;
    
    const analysis = new Map();
    
    // Domain analysis
    if (domain.includes('github.com')) analysis.set('technology', 0.8);
    if (domain.includes('linkedin.com')) analysis.set('business', 0.9);
    if (domain.includes('youtube.com')) analysis.set('entertainment', 0.9);
    if (domain.includes('twitter.com')) analysis.set('social', 0.9);
    if (domain.includes('amazon.com')) analysis.set('shopping', 0.9);
    
    // Path analysis
    if (path.includes('/news')) analysis.set('news', 0.7);
    if (path.includes('/health')) analysis.set('health', 0.7);
    if (path.includes('/finance')) analysis.set('finance', 0.7);
    if (path.includes('/travel')) analysis.set('travel', 0.7);
    
    return analysis;
  }

  // Analyze title content
  analyzeTitle(title) {
    const analysis = new Map();
    const words = title.toLowerCase().split(/\s+/);
    
    // Keyword mapping
    const keywordMap = {
      'tech': 'technology',
      'programming': 'technology',
      'code': 'technology',
      'business': 'business',
      'market': 'business',
      'learn': 'education',
      'course': 'education',
      'video': 'entertainment',
      'movie': 'entertainment',
      'news': 'news',
      'update': 'news',
      'social': 'social',
      'community': 'social',
      'shop': 'shopping',
      'buy': 'shopping',
      'health': 'health',
      'medical': 'health',
      'money': 'finance',
      'invest': 'finance',
      'travel': 'travel',
      'trip': 'travel'
    };
    
    words.forEach(word => {
      if (keywordMap[word]) {
        const category = keywordMap[word];
        analysis.set(category, (analysis.get(category) || 0) + 0.5);
      }
    });
    
    return analysis;
  }

  // Combine URL and title analysis
  combineAnalysis(urlAnalysis, titleAnalysis) {
    const combined = new Map();
    
    // Merge URL analysis
    urlAnalysis.forEach((score, category) => {
      const weight = this.weights.get(category) || 1.0;
      combined.set(category, score * weight);
    });
    
    // Merge title analysis
    titleAnalysis.forEach((score, category) => {
      const weight = this.weights.get(category) || 1.0;
      const currentScore = combined.get(category) || 0;
      combined.set(category, currentScore + (score * weight));
    });
    
    // Normalize scores
    const maxScore = Math.max(...combined.values());
    combined.forEach((score, category) => {
      combined.set(category, score / maxScore);
    });
    
    return combined;
  }

  // Get top categories for a bookmark
  getTopCategories(analysis, limit = 3) {
    return Array.from(analysis.entries())
      .sort((a, b) => b[1] - a[1])
      .slice(0, limit)
      .map(([category, score]) => ({
        category,
        score: Math.round(score * 100) / 100
      }));
  }
}

// Export the module
export default OSOMIntegration; 