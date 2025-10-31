#!/usr/bin/env python3
"""
Unified Bookmark Exporter
Export Chrome bookmarks to Notion, Obsidian, or XMind format.

Usage:
    python bookmark_exporter.py --format notion --token <token> --database <db_id>
    python bookmark_exporter.py --format obsidian --output ./vault/bookmarks
    python bookmark_exporter.py --format xmind --output bookmarks.xmind
    python bookmark_exporter.py --format json --output bookmarks.json
"""

import json
import os
import platform
import argparse
from pathlib import Path
from typing import Dict, List, Optional


class BookmarkLoader:
    """Load and parse Chrome bookmarks."""
    
    @staticmethod
    def get_default_bookmarks_path() -> str:
        """Get the default Chrome bookmarks path for the current OS."""
        system = platform.system()
        user = os.getlogin()
        
        paths = {
            "Windows": f"C:\\Users\\{user}\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Bookmarks",
            "Linux": f"/home/{user}/.config/google-chrome/Default/Bookmarks",
            "Darwin": f"/Users/{user}/Library/Application Support/Google/Chrome/Default/Bookmarks"
        }
        
        if system not in paths:
            raise OSError(f"Unsupported operating system: {system}")
        
        return paths[system]
    
    @staticmethod
    def load_bookmarks(path: Optional[str] = None) -> Dict:
        """Load bookmarks from JSON file."""
        if path is None:
            path = BookmarkLoader.get_default_bookmarks_path()
        
        try:
            with open(path, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Bookmarks file not found: {path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in bookmarks file: {e}")
    
    @staticmethod
    def extract_bookmarks_tree(data: Dict) -> List[Dict]:
        """Extract bookmarks as a hierarchical structure."""
        def process_node(node: Dict, path: str = "") -> List[Dict]:
            results = []
            
            if node.get("url"):
                results.append({
                    "title": node.get("name", "Untitled"),
                    "url": node["url"],
                    "path": path,
                    "date_added": node.get("date_added", 0)
                })
            
            if "children" in node:
                folder_name = node.get("name", "")
                new_path = f"{path}/{folder_name}" if path else folder_name
                
                for child in node["children"]:
                    results.extend(process_node(child, new_path))
            
            return results
        
        bookmarks = []
        roots = data.get("roots", {})
        
        for root_name, root_node in roots.items():
            if isinstance(root_node, dict):
                bookmarks.extend(process_node(root_node))
        
        return bookmarks
    
    @staticmethod
    def extract_folders(data: Dict) -> List[str]:
        """Extract all folder names."""
        def get_folders(node: Dict) -> List[str]:
            folders = []
            
            if node.get("type") == "folder":
                folders.append(node.get("name", "Unnamed"))
                
                if "children" in node:
                    for child in node["children"]:
                        folders.extend(get_folders(child))
            
            return folders
        
        all_folders = []
        roots = data.get("roots", {})
        
        for root_node in roots.values():
            if isinstance(root_node, dict) and "children" in root_node:
                for child in root_node["children"]:
                    all_folders.extend(get_folders(child))
        
        return all_folders


class NotionExporter:
    """Export bookmarks to Notion."""
    
    def __init__(self, token: str, database_id: str):
        try:
            from notion_client import Client
            self.client = Client(auth=token)
            self.database_id = database_id
        except ImportError:
            raise ImportError("notion-client not installed. Run: pip install notion-client")
    
    def export(self, bookmarks: List[Dict]) -> Dict:
        """Export bookmarks to Notion database."""
        success_count = 0
        failed = []
        
        print(f"Exporting {len(bookmarks)} bookmarks to Notion...")
        
        for bookmark in bookmarks:
            try:
                self.client.pages.create(
                    parent={"database_id": self.database_id},
                    properties={
                        "Name": {
                            "title": [{"text": {"content": bookmark["title"]}}]
                        },
                        "URL": {
                            "url": bookmark["url"]
                        },
                        "Folder": {
                            "rich_text": [{"text": {"content": bookmark["path"]}}]
                        }
                    }
                )
                success_count += 1
                print(f"✓ {bookmark['title']}")
            except Exception as e:
                failed.append({"bookmark": bookmark, "error": str(e)})
                print(f"✗ {bookmark['title']}: {e}")
        
        return {
            "success": success_count,
            "failed": len(failed),
            "errors": failed
        }


class ObsidianExporter:
    """Export bookmarks to Obsidian markdown format."""
    
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def export(self, bookmarks: List[Dict]) -> Dict:
        """Export bookmarks as markdown files."""
        # Group by folder
        by_folder = {}
        for bookmark in bookmarks:
            folder = bookmark["path"] or "Unfiled"
            if folder not in by_folder:
                by_folder[folder] = []
            by_folder[folder].append(bookmark)
        
        print(f"Exporting {len(bookmarks)} bookmarks to Obsidian...")
        
        # Create one file per folder
        for folder, items in by_folder.items():
            filename = folder.replace("/", " - ") + ".md"
            filepath = self.output_dir / filename
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"# {folder}\n\n")
                
                for item in items:
                    f.write(f"- [{item['title']}]({item['url']})\n")
            
            print(f"✓ Created {filename}")
        
        return {
            "files_created": len(by_folder),
            "bookmarks_exported": len(bookmarks),
            "output_directory": str(self.output_dir)
        }


class XMindExporter:
    """Export bookmarks to XMind format."""
    
    def __init__(self, output_file: str):
        self.output_file = output_file
        try:
            import xmind
            self.xmind = xmind
        except ImportError:
            raise ImportError("xmind not installed. Run: pip install xmind")
    
    def export(self, bookmarks: List[Dict]) -> Dict:
        """Export bookmarks as XMind mind map."""
        workbook = self.xmind.load(self.output_file)
        sheet = workbook.getPrimarySheet()
        sheet.setTitle("Chrome Bookmarks")
        
        root_topic = sheet.getRootTopic()
        root_topic.setTitle("My Bookmarks")
        
        # Group by top-level folder
        by_folder = {}
        for bookmark in bookmarks:
            parts = bookmark["path"].split("/") if bookmark["path"] else ["Unfiled"]
            top_folder = parts[0]
            
            if top_folder not in by_folder:
                by_folder[top_folder] = []
            by_folder[top_folder].append(bookmark)
        
        print(f"Exporting {len(bookmarks)} bookmarks to XMind...")
        
        # Create topics
        for folder, items in by_folder.items():
            folder_topic = root_topic.addSubTopic()
            folder_topic.setTitle(folder)
            
            for item in items:
                bookmark_topic = folder_topic.addSubTopic()
                bookmark_topic.setTitle(item["title"])
                bookmark_topic.setURLHyperlink(item["url"])
            
            print(f"✓ Added folder: {folder} ({len(items)} bookmarks)")
        
        self.xmind.save(workbook, self.output_file)
        
        return {
            "bookmarks_exported": len(bookmarks),
            "folders": len(by_folder),
            "output_file": self.output_file
        }


class JSONExporter:
    """Export bookmarks to JSON format."""
    
    def __init__(self, output_file: str):
        self.output_file = output_file
    
    def export(self, bookmarks: List[Dict]) -> Dict:
        """Export bookmarks as JSON."""
        with open(self.output_file, "w", encoding="utf-8") as f:
            json.dump(bookmarks, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Exported {len(bookmarks)} bookmarks to {self.output_file}")
        
        return {
            "bookmarks_exported": len(bookmarks),
            "output_file": self.output_file
        }


def main():
    parser = argparse.ArgumentParser(
        description="Export Chrome bookmarks to various formats",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Export to Notion
  python bookmark_exporter.py --format notion --token secret_xxx --database abc123
  
  # Export to Obsidian
  python bookmark_exporter.py --format obsidian --output ./vault/bookmarks
  
  # Export to XMind
  python bookmark_exporter.py --format xmind --output bookmarks.xmind
  
  # Export to JSON
  python bookmark_exporter.py --format json --output bookmarks.json
  
  # Use custom bookmarks file
  python bookmark_exporter.py --format json --input ~/custom_bookmarks.json --output out.json
        """
    )
    
    parser.add_argument(
        "--format",
        required=True,
        choices=["notion", "obsidian", "xmind", "json"],
        help="Export format"
    )
    
    parser.add_argument(
        "--input",
        help="Path to bookmarks file (default: auto-detect Chrome bookmarks)"
    )
    
    parser.add_argument(
        "--output",
        help="Output file or directory"
    )
    
    parser.add_argument(
        "--token",
        help="Notion integration token (required for Notion export)"
    )
    
    parser.add_argument(
        "--database",
        help="Notion database ID (required for Notion export)"
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.format == "notion":
        if not args.token or not args.database:
            parser.error("Notion export requires --token and --database")
    elif args.format in ["obsidian", "xmind", "json"]:
        if not args.output:
            parser.error(f"{args.format.capitalize()} export requires --output")
    
    try:
        # Load bookmarks
        print("Loading bookmarks...")
        loader = BookmarkLoader()
        data = loader.load_bookmarks(args.input)
        bookmarks = loader.extract_bookmarks_tree(data)
        
        print(f"Found {len(bookmarks)} bookmarks\n")
        
        # Export
        if args.format == "notion":
            exporter = NotionExporter(args.token, args.database)
            result = exporter.export(bookmarks)
            print(f"\n✓ Export complete: {result['success']} succeeded, {result['failed']} failed")
        
        elif args.format == "obsidian":
            exporter = ObsidianExporter(args.output)
            result = exporter.export(bookmarks)
            print(f"\n✓ Export complete: {result['files_created']} files created in {result['output_directory']}")
        
        elif args.format == "xmind":
            exporter = XMindExporter(args.output)
            result = exporter.export(bookmarks)
            print(f"\n✓ Export complete: {result['folders']} folders created in {result['output_file']}")
        
        elif args.format == "json":
            exporter = JSONExporter(args.output)
            result = exporter.export(bookmarks)
            print(f"\n✓ Export complete: {result['output_file']}")
    
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())