# Installation Guide

## Quick Start

### Prerequisites

- Google Chrome (version 88 or higher)
- Git (optional, for cloning)

### Step 1: Get the Code

**Option A: Clone the repository**
```bash
git clone https://github.com/MarlinZH/chrome_bookmark_manager.git
cd chrome_bookmark_manager
```

**Option B: Download ZIP**
1. Go to the [GitHub repository](https://github.com/MarlinZH/chrome_bookmark_manager)
2. Click "Code" → "Download ZIP"
3. Extract the ZIP file to a location of your choice

### Step 2: Load the Extension

1. Open Chrome and navigate to `chrome://extensions/`
2. Enable "Developer mode" (toggle in the top right)
3. Click "Load unpacked"
4. Navigate to the `extension` folder inside the project directory
5. Click "Select Folder"

### Step 3: Verify Installation

You should see:
- The extension appears in your extensions list
- An icon appears in your Chrome toolbar
- No error messages

## Python Scripts (Optional)

If you want to use the Python export scripts:

### Step 1: Install Python

Ensure you have Python 3.7 or higher:
```bash
python --version
```

### Step 2: Install Dependencies

```bash
cd chrome_bookmark_manager
pip install -r requirements.txt
```

### Step 3: Download NLTK Data (Optional)

If using NLP features:
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

### Step 4: Install SpaCy Model (Optional)

For advanced text analysis:
```bash
python -m spacy download en_core_web_sm
```

## Notion Setup

To use the Notion integration:

### Step 1: Create a Notion Integration

1. Go to [https://www.notion.so/my-integrations](https://www.notion.so/my-integrations)
2. Click "+ New integration"
3. Give it a name: "Bookmark Manager"
4. Select your workspace
5. Click "Submit"
6. Copy the "Internal Integration Token" (starts with `secret_`)

### Step 2: Create a Database

1. In Notion, create a new page
2. Add a "Database - Full page" block
3. Name it "Bookmarks" (or any name you prefer)
4. Add these properties:
   - **Name** (Title) - Already exists
   - **URL** (URL type)
   - **Folder** (Text type)

### Step 3: Share Database with Integration

1. Click "Share" button in your database
2. Click "Invite"
3. Select your integration "Bookmark Manager"
4. Click "Invite"

### Step 4: Get Database ID

1. Open your database as a full page
2. Copy the URL
3. The Database ID is the long string in the URL:
   ```
   https://notion.so/workspace/DATABASE_ID?v=...
   ```
   Extract just the `DATABASE_ID` part (32 characters, letters and numbers)

### Step 5: Configure Extension

1. Click the extension icon
2. Paste your Integration Token
3. Paste your Database ID
4. Click "Save"
5. Look for the "Saved securely!" message

## Troubleshooting

### Extension Won't Load

**Problem**: "Manifest file is missing or unreadable"
- **Solution**: Make sure you're selecting the `extension` folder, not the root folder

**Problem**: "Invalid manifest"
- **Solution**: Ensure all files were extracted/cloned correctly

### Icons Not Showing

**Problem**: Extension icon is blank
- **Solution**: Check that the `extension/icons/` folder contains the icon files

### Python Errors

**Problem**: `ModuleNotFoundError`
- **Solution**: Install dependencies: `pip install -r requirements.txt`

**Problem**: NLTK download fails
- **Solution**: Try manual download:
  ```python
  python -c "import nltk; nltk.download('punkt', quiet=False); nltk.download('stopwords', quiet=False)"
  ```

### Notion Connection Fails

**Problem**: "Failed to export to Notion"
- **Solution 1**: Verify your Integration Token is correct
- **Solution 2**: Ensure database is shared with integration
- **Solution 3**: Check Database ID is exactly 32 characters
- **Solution 4**: Verify database properties match expected names

## Updating

To update to the latest version:

1. **Git users**:
   ```bash
   cd chrome_bookmark_manager
   git pull origin main
   ```

2. **ZIP users**:
   - Download the latest ZIP
   - Extract to the same location (overwrite old files)

3. **Reload extension**:
   - Go to `chrome://extensions/`
   - Click the refresh icon on the extension card

## Uninstalling

### Remove Extension

1. Go to `chrome://extensions/`
2. Find "AI Bookmark Manager"
3. Click "Remove"
4. Confirm removal

### Clean Up Data

The extension stores encrypted data in Chrome's local storage. This is automatically removed when you uninstall the extension.

If you want to manually clear it first:
1. Click the extension icon
2. Click "Clear" button in the Notion section
3. Then uninstall the extension

## Next Steps

- Read the [Usage Guide](../README.md#usage)
- Review [Security Information](SECURITY.md)
- Check out [Examples](../examples/)
- Report issues on [GitHub](https://github.com/MarlinZH/chrome_bookmark_manager/issues)

## Need Help?

If you're stuck:
1. Check the [Troubleshooting](#troubleshooting) section above
2. Review the main [README](../README.md)
3. Search [existing issues](https://github.com/MarlinZH/chrome_bookmark_manager/issues)
4. Create a [new issue](https://github.com/MarlinZH/chrome_bookmark_manager/issues/new) with:
   - What you were trying to do
   - What happened instead
   - Error messages (if any)
   - Your Chrome version
   - Your operating system