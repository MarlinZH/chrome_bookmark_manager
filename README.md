# AI Bookmark Manager Chrome Extension

An intelligent Chrome extension that helps you organize and manage your bookmarks using AI-powered analysis, part of the OSOM AI framework. Export your bookmarks to Notion, Obsidian, or XMind for better organization.

![Chrome Extension](https://img.shields.io/badge/Chrome-Extension-brightgreen)
![Version](https://img.shields.io/badge/version-1.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## 🌟 Features

- **AI-Powered Analysis**: Automatically categorize bookmarks using intelligent URL and title analysis
- **Smart Recommendations**: Get suggestions for organizing your bookmarks into logical folders
- **Notion Integration**: Export bookmarks directly to your Notion databases
- **Multiple Export Formats**: Support for Notion, Obsidian, and XMind
- **Modern UI**: Clean, user-friendly interface built with Tailwind CSS
- **Real-time Processing**: Analyze and organize bookmarks on-the-fly

## 📋 Prerequisites

Before installing this extension, ensure you have:

- **Google Chrome** (version 88 or higher)
- **Python 3.7+** (for Python scripts)
- **Node.js** (optional, for development)

### Python Dependencies

The Python scripts require the following packages:

```bash
pip install -r requirements.txt
```

Required packages:
- `pandas` - Data manipulation
- `notion-client` - Notion API integration
- `spacy` - Natural language processing (optional)
- `nltk` - Text processing (optional)
- `xmind` - XMind file generation

### SpaCy Language Model (Optional)

If you plan to use advanced NLP features:

```bash
python -m spacy download en_core_web_sm
```

## 🚀 Installation

### Chrome Extension

1. **Clone or download this repository**:
   ```bash
   git clone https://github.com/MarlinZH/chrome_bookmark_manager.git
   cd chrome_bookmark_manager
   ```

2. **Open Chrome Extensions page**:
   - Navigate to `chrome://extensions/`
   - Or: Menu → More Tools → Extensions

3. **Enable Developer Mode**:
   - Toggle the "Developer mode" switch in the top right corner

4. **Load the extension**:
   - Click "Load unpacked"
   - Select the `chrome_bookmark_manager` directory
   - The extension icon should appear in your Chrome toolbar

### Python Scripts

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables** (for Notion integration):
   ```bash
   export NOTION_TOKEN="your_notion_integration_token"
   export DATABASE_ID="your_notion_database_id"
   ```

## 📖 Usage

### Using the Chrome Extension

1. **Click the extension icon** in your Chrome toolbar

2. **Analyze Bookmarks**:
   - Click the "Analyze Bookmarks" button
   - Wait for the AI to categorize your bookmarks
   - View suggested categories and organization recommendations

3. **Create Folders**:
   - Select a recommended category or enter a custom name
   - Click "Create" to add a new bookmark folder

4. **Browse Bookmarks**:
   - Click on any folder to view its bookmarks
   - Bookmarks are displayed with clickable links

### Notion Integration Setup

1. **Create a Notion Integration**:
   - Go to [Notion Integrations](https://www.notion.so/my-integrations)
   - Click "+ New integration"
   - Give it a name (e.g., "Bookmark Manager")
   - Copy the "Internal Integration Token"

2. **Share your database with the integration**:
   - Open your Notion database
   - Click "Share" in the top right
   - Invite your integration

3. **Get your Database ID**:
   - Open your database in a browser
   - Copy the URL
   - Extract the ID (the long string between `/` and `?`)
   - Example: `https://notion.so/workspace/DATABASE_ID?v=...`

4. **Configure the extension**:
   - Paste your Integration Token
   - Paste your Database ID
   - Click "Save"
   - Click "Export to Notion"

### Using Python Scripts

#### Export to Notion

```bash
python Bookmarks_to_Notion.py
```

This script will automatically:
- Detect your Chrome bookmarks file location
- Extract all bookmark folders
- Export them to your Notion database

#### Export to Obsidian

```bash
python Bookmarks_to_Obsidian.py
```

#### Export to XMind

```bash
python Bookmarks_to_XMind.py
```

#### Manual Processing

For more control, use `main.py`:

```bash
python main.py
```

You'll be prompted for:
- Path to your bookmarks file
- Notion integration token
- Notion database ID

### Finding Your Bookmarks File

Chrome bookmarks are typically located at:

- **Windows**: `C:\Users\[Username]\AppData\Local\Google\Chrome\User Data\Default\Bookmarks`
- **macOS**: `/Users/[Username]/Library/Application Support/Google/Chrome/Default/Bookmarks`
- **Linux**: `/home/[Username]/.config/google-chrome/Default/Bookmarks`

## 🏗️ Project Structure

```
chrome_bookmark_manager/
├── manifest.json              # Chrome extension manifest
├── popup.html                 # Extension popup interface
├── popup.js                   # Main popup logic
├── background.js              # Background service worker
├── style.css                  # Custom styles
├── icons/                     # Extension icons
│   ├── icon16.png
│   ├── icon48.png
│   └── icon128.png
├── osom-integration.js        # OSOM AI categorization engine
├── notion-integration.js      # Notion API wrapper
├── main.py                    # Main Python script
├── Bookmarks_to_Notion.py     # Notion export utility
├── Bookmarks_to_Obsidian.py   # Obsidian export utility
├── Bookmarks_to_XMind.py      # XMind export utility
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🔧 Development

The extension is built using:

- **HTML/CSS**: Interface structure
- **Tailwind CSS**: Utility-first styling
- **JavaScript (ES6+)**: Core logic
- **Chrome Extension APIs**: Browser integration
- **Python**: Data processing and exports

### Technology Stack

#### Frontend
- Chrome Manifest V3
- ES6 Modules
- Tailwind CSS (CDN)
- Chrome Bookmarks API
- Chrome Storage API

#### Backend
- Python 3.7+
- Notion API
- SpaCy NLP (optional)
- NLTK (optional)

### Key Components

#### OSOM Integration (`osom-integration.js`)

The OSOM (Open Source Organization Manager) engine analyzes bookmarks based on:
- URL domain patterns
- URL path analysis
- Title keyword extraction
- Weighted scoring system

Supported categories:
- Technology
- Business
- Education
- Entertainment
- News
- Social
- Shopping
- Health
- Finance
- Travel

#### Notion Integration (`notion-integration.js`)

Handles communication with the Notion API to:
- Create database entries
- Organize bookmarks by folder
- Maintain folder hierarchy

## 🔒 Security & Privacy

### Data Storage

- **Notion tokens** are stored in Chrome's local storage
- **No data** is sent to external servers (except Notion when explicitly requested)
- **All processing** happens locally in your browser

### Important Security Notes

⚠️ **Warning**: API tokens stored in Chrome's local storage are not encrypted. Keep your tokens secure and:
- Don't share your Chrome profile
- Don't commit tokens to version control
- Regularly rotate your Notion integration tokens
- Only grant necessary permissions to integrations

## 🐛 Troubleshooting

### Extension Not Loading

- Ensure Developer Mode is enabled in Chrome
- Check the console for errors: Right-click extension icon → Inspect popup
- Verify all files are present in the extension directory

### Bookmarks Not Analyzing

- Check browser console for JavaScript errors
- Ensure you have bookmarks to analyze
- Try refreshing the extension

### Notion Export Failing

- Verify your Integration Token is correct
- Ensure the database is shared with your integration
- Check that the Database ID is correct
- Verify network connectivity

### Python Scripts Not Working

```bash
# Verify Python version
python --version  # Should be 3.7+

# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Check environment variables
echo $NOTION_TOKEN
echo $DATABASE_ID
```

### Common Issues

**Issue**: "File not found" error
- **Solution**: Verify the bookmarks file path for your OS

**Issue**: "Invalid JSON" error
- **Solution**: Chrome bookmarks file may be corrupted; check Chrome settings

**Issue**: NLTK data not found
- **Solution**: Run the download commands again:
  ```python
  import nltk
  nltk.download('punkt')
  nltk.download('stopwords')
  ```

## 🔄 Future Improvements

- [ ] Cloud sync for settings and categories
- [ ] Custom categorization rules
- [ ] Machine learning for improved categorization
- [ ] Bulk bookmark operations
- [ ] Import from other browsers
- [ ] Export to more formats (CSV, JSON, etc.)
- [ ] Dark mode support
- [ ] Multi-language support
- [ ] Duplicate detection
- [ ] Broken link checker
- [ ] Chrome Web Store publication

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Contribution Guidelines

- Follow existing code style
- Add comments for complex logic
- Test thoroughly before submitting
- Update documentation as needed
- Include screenshots for UI changes

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**MarlinZH**
- GitHub: [@MarlinZH](https://github.com/MarlinZH)

## 🙏 Acknowledgments

- Chrome Extensions documentation
- Notion API team
- Tailwind CSS community
- Contributors and testers

## 📞 Support

If you encounter issues or have questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Search existing [GitHub Issues](https://github.com/MarlinZH/chrome_bookmark_manager/issues)
3. Create a new issue with:
   - Detailed description
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - Chrome version and OS

## 📊 Version History

### Version 1.0 (Current)
- Initial release
- AI-powered bookmark analysis
- Notion integration
- Multiple export formats
- Modern UI with Tailwind CSS

---

**Note**: This project is under active development. Star the repository to stay updated with new features and improvements!
