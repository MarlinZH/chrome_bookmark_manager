import json
import pandas as pd
from notion_client import Client
import spacy
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
import nltk
import os

# Initialize NLTK
try:
    nltk.download("punkt", quiet=True)
    nltk.download("stopwords", quiet=True)
except Exception as e:
    print(f"Warning: NLTK download failed: {e}")


def load_bookmarks(bookmarks_path):
    """Load bookmarks from a JSON file.
    
    Args:
        bookmarks_path (str): Path to the bookmarks JSON file
        
    Returns:
        dict: Parsed bookmarks data or None if error occurs
    """
    try:
        with open(bookmarks_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File not found at {bookmarks_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format - {e}")
        return None
    except Exception as e:
        print(f"Error loading bookmarks: {e}")
        return None


def extract_folders(children):
    """Recursively extract folder names from bookmark structure.
    
    Args:
        children (list): List of bookmark children nodes
        
    Returns:
        list: List of folder names
    """
    folders = []
    for child in children:
        if child.get("type") == "folder":
            folders.append(child["name"])
            if "children" in child:
                folders.extend(extract_folders(child.get("children", [])))
    return folders


def organize_bookmarks(bookmarks_data):
    """Organize bookmarks by folder.
    
    Args:
        bookmarks_data (dict): Parsed bookmarks JSON data
        
    Returns:
        dict: Dictionary mapping folder names to list of bookmarks
    """
    try:
        bookmark_bar = bookmarks_data.get("roots", {}).get("bookmark_bar", {})
        organized = {}
        
        for folder in bookmark_bar.get("children", []):
            if folder.get("type") == "folder":
                folder_name = folder.get("name", "Unnamed Folder")
                bookmarks = [
                    bookmark.get("name", bookmark.get("url", "Unnamed Bookmark"))
                    for bookmark in folder.get("children", [])
                    if bookmark.get("url")
                ]
                organized[folder_name] = bookmarks
        
        return organized
    except Exception as e:
        print(f"Error organizing bookmarks: {e}")
        return {}


def analyze_bookmarks_with_spacy(bookmarks, nlp_model):
    """Analyze bookmark titles using spaCy NLP.
    
    Args:
        bookmarks (list): List of bookmark dictionaries
        nlp_model: Loaded spaCy language model
        
    Returns:
        list: Bookmarks with added entity information
    """
    try:
        for bookmark in bookmarks:
            title = bookmark.get("title", "")
            if title:
                doc = nlp_model(title)
                bookmark["entities"] = [ent.text for ent in doc.ents]
            else:
                bookmark["entities"] = []
        return bookmarks
    except Exception as e:
        print(f"Error analyzing bookmarks with spaCy: {e}")
        return bookmarks


def extract_keywords(text):
    """Extract keywords from text by removing stopwords.
    
    Args:
        text (str): Input text to analyze
        
    Returns:
        list: List of extracted keywords
    """
    try:
        tokens = word_tokenize(text)
        stop_words = set(stopwords.words("english"))
        return [
            word.lower()
            for word in tokens
            if word.isalpha() and word.lower() not in stop_words
        ]
    except Exception as e:
        print(f"Error extracting keywords: {e}")
        return []


def group_bookmarks(bookmarks):
    """Group bookmarks by extracted keywords.
    
    Args:
        bookmarks (dict): Dictionary of bookmark titles and content
        
    Returns:
        dict: Dictionary mapping keywords to list of bookmark titles
    """
    folders = defaultdict(list)
    try:
        for title, content in bookmarks.items():
            keywords = extract_keywords(content)
            for keyword in keywords:
                folders[keyword].append(title)
    except Exception as e:
        print(f"Error grouping bookmarks: {e}")
    return dict(folders)


def import_to_notion(bookmarks_folders, notion_token, database_id):
    """Import folder names to Notion database.
    
    Args:
        bookmarks_folders (list): List of folder names
        notion_token (str): Notion API integration token
        database_id (str): Notion database ID
    """
    try:
        notion = Client(auth=notion_token)
        success_count = 0
        
        for folder in bookmarks_folders:
            try:
                notion.pages.create(
                    parent={"database_id": database_id},
                    properties={"Name": {"title": [{"text": {"content": folder}}]}},
                )
                success_count += 1
                print(f"✓ Imported folder: {folder}")
            except Exception as e:
                print(f"✗ Failed to import folder '{folder}': {e}")
        
        print(f"\nSuccessfully imported {success_count}/{len(bookmarks_folders)} folders")
    except Exception as e:
        print(f"Error connecting to Notion: {e}")


def main():
    """Main function to process bookmarks and export to Notion."""
    print("Chrome Bookmark Manager - Main Script")
    print("=" * 50)
    
    # User inputs
    bookmarks_path = input("Enter the path to your bookmarks file: ").strip()
    notion_token = input("Enter your Notion integration token: ").strip()
    database_id = input("Enter your Notion database ID: ").strip()

    # Validate inputs
    if not bookmarks_path or not notion_token or not database_id:
        print("Error: All fields are required.")
        return

    # Load bookmarks
    print("\nLoading bookmarks...")
    bookmarks_data = load_bookmarks(bookmarks_path)
    if not bookmarks_data:
        return

    # Organize and display bookmarks
    print("\nOrganizing bookmarks...")
    organized_bookmarks = organize_bookmarks(bookmarks_data)
    
    if organized_bookmarks:
        print("\nOrganized Bookmarks by Folder:")
        print("-" * 50)
        for folder, bookmarks in organized_bookmarks.items():
            print(f"\n📁 {folder}")
            print(f"   Bookmarks: {len(bookmarks)}")
            if bookmarks:
                sample = bookmarks[0]
                print(f"   Sample: {sample[:60]}..." if len(sample) > 60 else f"   Sample: {sample}")
    else:
        print("No organized bookmarks found.")

    # Extract folder names
    print("\nExtracting folder structure...")
    folder_names = extract_folders(
        bookmarks_data.get("roots", {}).get("bookmark_bar", {}).get("children", [])
    )
    
    if folder_names:
        print(f"\nFound {len(folder_names)} folders:")
        df = pd.DataFrame(folder_names, columns=["Folders"])
        print(df.to_string(index=False))
        
        # Import to Notion
        print("\nImporting to Notion...")
        import_to_notion(folder_names, notion_token, database_id)
    else:
        print("No folders found to import.")

    print("\n" + "=" * 50)
    print("Process completed!")


if __name__ == "__main__":
    main()