# Python Bookmark Export Scripts

Unified tool for exporting Chrome bookmarks to various formats.

## Quick Start

### Install Dependencies

```bash
pip install -r ../requirements.txt
```

### Usage

#### Export to Notion

```bash
python bookmark_exporter.py --format notion \
  --token secret_xxxx \
  --database abc123def456
```

#### Export to Obsidian

```bash
python bookmark_exporter.py --format obsidian \
  --output ~/Documents/ObsidianVault/Bookmarks
```

#### Export to XMind

```bash
python bookmark_exporter.py --format xmind \
  --output my_bookmarks.xmind
```

#### Export to JSON

```bash
python bookmark_exporter.py --format json \
  --output bookmarks.json
```

### Custom Bookmarks File

```bash
python bookmark_exporter.py --format json \
  --input ~/custom/Bookmarks \
  --output output.json
```

## File Structure

- `bookmark_exporter.py` - Unified export tool (NEW - replaces all separate scripts)
- `main.py` - Legacy interactive script (kept for compatibility)
- `bookmarks_to_notion.py` - Legacy auto-export script (kept for compatibility)

## Environment Variables

For Notion export, you can also use environment variables:

```bash
export NOTION_TOKEN="secret_xxxx"
export DATABASE_ID="abc123def456"

python bookmark_exporter.py --format notion
```

## Features

### Notion Export
- Creates pages in specified database
- Includes title, URL, and folder path
- Progress indicator
- Error handling

### Obsidian Export
- One markdown file per folder
- Proper markdown link format
- Organized by folder structure

### XMind Export
- Mind map visualization
- Hierarchical folder structure
- Clickable URLs in topics

### JSON Export
- Complete bookmark data
- Easy to process programmatically
- Includes metadata

## Requirements

- **All formats**: Python 3.7+
- **Notion**: `notion-client`
- **XMind**: `xmind`
- **Obsidian & JSON**: No extra dependencies

## Troubleshooting

### Bookmarks File Not Found

The script auto-detects Chrome bookmarks location. If it fails:

```bash
python bookmark_exporter.py --format json \
  --input "/path/to/Bookmarks" \
  --output output.json
```

### Notion Export Fails

1. Verify integration token is correct
2. Ensure database is shared with integration
3. Check database ID is 32 characters
4. Verify database has Name (title), URL (url), and Folder (text) properties

### Module Not Found

```bash
pip install notion-client xmind
```

## Migration from Old Scripts

### Old Way (Multiple Scripts)

```bash
python Bookmarks_to_Notion.py
python Bookmarks_to_Obsidian.py
python Bookmarks_to_XMind.py
```

### New Way (One Script)

```bash
python bookmark_exporter.py --format notion --token xxx --database yyy
python bookmark_exporter.py --format obsidian --output ./vault
python bookmark_exporter.py --format xmind --output map.xmind
```

## Benefits of Unified Tool

- ✅ Single script to maintain
- ✅ Consistent interface
- ✅ Better error handling
- ✅ More features (JSON export, custom input)
- ✅ Command-line arguments
- ✅ Progress indicators
- ✅ Easier to use

## Legacy Scripts

The old scripts are kept for backward compatibility but are deprecated:

- `main.py` - Use `bookmark_exporter.py --format notion` instead
- `bookmarks_to_notion.py` - Use `bookmark_exporter.py --format notion` instead

**Note**: Old scripts at project root will be removed in v1.2.0