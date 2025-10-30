# AI Bookmark Manager Chrome Extension

An intelligent Chrome extension that helps you organize and manage your bookmarks using AI-powered analysis, part of the OSOM AI framework. Export your bookmarks to Notion, Obsidian, or XMind for better organization.

![Chrome Extension](https://img.shields.io/badge/Chrome-Extension-brightgreen)
![Version](https://img.shields.io/badge/version-1.1.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Security](https://img.shields.io/badge/security-AES--256--GCM-red)

## 🌟 Features

- **AI-Powered Analysis**: Automatically categorize bookmarks using intelligent URL and title analysis
- **Smart Recommendations**: Get suggestions for organizing your bookmarks into logical folders  
- **🔐 Encrypted Credential Storage**: AES-256-GCM encryption for secure Notion token storage
- **Notion Integration**: Export bookmarks directly to your Notion databases
- **Multiple Export Formats**: Support for Notion, Obsidian, and XMind
- **Modern UI**: Clean, user-friendly interface built with Tailwind CSS
- **Real-time Processing**: Analyze and organize bookmarks on-the-fly

## 🏗️ Project Structure

```
chrome_bookmark_manager/
├── extension/                  # Chrome extension files
│   ├── manifest.json          # Extension manifest
│   ├── popup.html             # Popup interface
│   ├── background.js          # Background service worker
│   ├── icons/                 # Extension icons
│   │   ├── icon16.png
│   │   ├── icon48.png
│   │   └── icon128.png
│   ├── js/                    # JavaScript modules
│   │   ├── popup.js           # Main popup logic
│   │   └── crypto.js          # 🔐 Encryption utilities
│   ├── integrations/          # Integration modules
│   │   ├── osom-integration.js    # AI categorization engine
│   │   └── notion-integration.js  # Notion API wrapper
│   └── styles/                # Stylesheets
│       └── popup.css          # Custom styles
│
├── python_scripts/            # Python utilities
│   ├── main.py                # Main processing script
│   └── bookmarks_to_notion.py # Notion export utility
│
├── docs/                      # Documentation
│   ├── SECURITY.md            # Security information
│   └── INSTALLATION.md        # Installation guide
│
├── requirements.txt           # Python dependencies
├── CHANGELOG.md               # Version history
└── README.md                  # This file
```

## 🔐 Security Features (NEW!)

### Encrypted Credential Storage

Version 1.1.0 introduces **AES-256-GCM encryption** for protecting your Notion API credentials:

- **Encryption Algorithm**: AES-256-GCM (industry standard)
- **Key Derivation**: SHA-256 hash of extension ID + salt
- **IV**: Random 96-bit initialization vector per encryption
- **Storage**: Encrypted data stored in Chrome local storage

#### How It Works

1. When you save credentials, they are encrypted using Web Crypto API
2. The encryption key is derived from your unique extension installation ID
3. Data is encrypted with AES-GCM and a random IV
4. Only the encrypted ciphertext is stored
5. Credentials are decrypted only when needed

#### Security Benefits

✅ **Before (v1.0)**:
- Plain text storage
- Readable by any script
- Visible in DevTools

✅ **After (v1.1)**:
- AES-256-GCM encrypted
- Requires decryption key
- Not visible in plain text
- Protected from casual inspection

**Read more**: [docs/SECURITY.md](docs/SECURITY.md)

## 📋 Prerequisites

- **Google Chrome** (version 88 or higher)
- **Python 3.7+** (optional, for Python scripts)

## 🚀 Quick Start

### Install the Extension

1. **Clone or download**:
   ```bash
   git clone https://github.com/MarlinZH/chrome_bookmark_manager.git
   cd chrome_bookmark_manager
   ```

2. **Load in Chrome**:
   - Navigate to `chrome://extensions/`
   - Enable \"Developer mode\"
   - Click \"Load unpacked\"
   - Select the `extension` folder

3. **Done!** The extension icon appears in your toolbar.

**Detailed instructions**: [docs/INSTALLATION.md](docs/INSTALLATION.md)

## 📖 Usage

### Analyzing Bookmarks

1. Click the extension icon
2. Click \"Analyze Bookmarks\"
3. View AI-generated categories
4. See recommended folder names

### Creating Folders

1. Select a recommended category OR enter a custom name
2. Click \"Create\"
3. Folder is added to your bookmarks

### Exporting to Notion

#### First Time Setup

1. **Create Notion Integration**: [notion.so/my-integrations](https://www.notion.so/my-integrations)
2. **Create Database**: Add a full-page database in Notion
3. **Share Database**: Invite your integration to the database
4. **Get Database ID**: Copy from the database URL

#### Export Process

1. Enter your Integration Token (encrypted on save)
2. Enter your Database ID
3. Click \"Save\" (credentials are encrypted with AES-256-GCM)
4. Click \"Export to Notion\"
5. Wait for completion message

### Clearing Credentials

For security, you can clear stored credentials:

1. Click \"Clear\" button in the Notion section
2. Confirm the action
3. Encrypted credentials are permanently removed

## 🔧 Development

### Technology Stack

**Extension**:
- Chrome Manifest V3
- JavaScript ES6 Modules
- Web Crypto API (for encryption)
- Tailwind CSS
- Chrome APIs (Bookmarks, Storage)

**Python Scripts**:
- Python 3.7+
- Notion API Client
- Pandas, NLTK, SpaCy (optional)

### Key Components

#### 🔐 CryptoManager (`extension/js/crypto.js`)

Handles all encryption/decryption:
- `encrypt(plaintext)` - Encrypt data with AES-GCM
- `decrypt(ciphertext)` - Decrypt data
- `secureStore(key, value)` - Encrypt and store
- `secureRetrieve(key)` - Retrieve and decrypt
- `secureRemove(key)` - Remove encrypted data

#### OSOM Integration (`extension/integrations/osom-integration.js`)

AI categorization engine that analyzes:
- URL domain patterns
- URL path structure
- Title keywords
- Weighted scoring

Categories: Technology, Business, Education, Entertainment, News, Social, Shopping, Health, Finance, Travel

#### Notion Integration (`extension/integrations/notion-integration.js`)

Notion API wrapper:
- Create pages in databases
- Batch import bookmarks
- Test connection
- Error handling

## 📊 Python Scripts

### Main Script

```bash
python python_scripts/main.py
```

Interactive script that:
- Loads Chrome bookmarks
- Organizes by folder
- Extracts folder structure
- Exports to Notion

### Auto-Export Script

```bash
# Set environment variables
export NOTION_TOKEN="your_token"
export DATABASE_ID="your_db_id"

# Run
python python_scripts/bookmarks_to_notion.py
```

Auto-detects bookmark location and exports.

## 🛡️ Security Best Practices

1. **Use Integration Tokens**: Create dedicated integrations, not personal tokens
2. **Limit Permissions**: Only grant necessary database access
3. **Rotate Regularly**: Change tokens periodically
4. **Clear When Done**: Use \"Clear\" button after exporting
5. **Lock Computer**: Always lock when away
6. **Don't Share Profile**: Keep Chrome profile private

**Full security details**: [docs/SECURITY.md](docs/SECURITY.md)

## 🐛 Troubleshooting

### Extension Issues

**Won't Load**: Ensure you selected the `extension` folder, not root  
**No Icon**: Check `extension/icons/` folder exists  
**Analysis Fails**: Check browser console for errors

### Notion Issues

**Export Fails**: 
- Verify token is correct
- Ensure database is shared with integration
- Check Database ID is 32 characters
- Verify database has Name, URL, and Folder properties

**Credentials Not Saving**:
- Check browser console for encryption errors
- Ensure Chrome supports Web Crypto API
- Try clearing and re-entering

### Python Issues

**Module Not Found**:
```bash
pip install -r requirements.txt
```

**NLTK Errors**:
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

## 🔄 Changelog

### [1.1.0] - 2025-10-30

#### Added
- 🔐 **AES-256-GCM encryption** for credential storage
- New `CryptoManager` class for encryption operations
- \"Clear\" button to remove stored credentials
- Comprehensive security documentation
- Installation guide
- Reorganized project structure

#### Changed
- Moved extension files to `extension/` directory
- Moved Python scripts to `python_scripts/` directory
- Updated manifest to version 1.1.0
- Improved UI with better feedback
- Enhanced error handling

#### Security
- Credentials now encrypted at rest
- Secure key derivation using extension ID
- Random IV generation per encryption
- Protection against casual data inspection

### [1.0.1] - 2025-10-30
- Fixed critical bugs
- Added comprehensive documentation
- Improved error handling

### [1.0.0] - 2023-12-24
- Initial release

**Full changelog**: [CHANGELOG.md](CHANGELOG.md)

## 🤝 Contributing

Contributions welcome!

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Guidelines

- Follow existing code style
- Add encryption for any new credential storage
- Test thoroughly
- Update documentation
- Include security considerations

## 📄 License

This project is licensed under the MIT License.

## 👤 Author

**MarlinZH**
- GitHub: [@MarlinZH](https://github.com/MarlinZH)

## 🙏 Acknowledgments

- Chrome Extensions documentation
- Web Crypto API
- Notion API team
- Tailwind CSS community
- Security reviewers and contributors

## 📞 Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/MarlinZH/chrome_bookmark_manager/issues)
- **Security**: See [SECURITY.md](docs/SECURITY.md)

---

**⭐ Star this repo** if you find it useful!

**🔐 Your credentials are now encrypted and protected!**
