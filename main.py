import json
import pandas as pd
from notion_client import Client
import spacy
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
import nltk
import os
import blob

# Initialize NLTK
nltk.download("punkt")
nltk.download("stopwords")
ii ~wate by --3


# Function to load bookmarks JSON
def load_bookmarks(bookmarks_path):
    try:
        with open(bookmarks_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error: {e}")
        return None


# Function to recursively extract folders
def extract_folders(children):
    folders = []
    for child in children:
        if child.get("type") == "folder":
            folders.append(child["name"])
            folders.extend(extract_folders(child.get("children", [])))
    return folders


# Organize bookmarks by folder
def organize_bookmarks(bookmarks_data):
    bookmark_bar = bookmarks_data.get("roots", {}).get("bookmark_bar", {})
    organized = {
        folder.get("name", ""): [
            bookmark.get("name", "") for bookmark in folder.get("children", [])
        ]
        for folder in bookmark_bar.get("children", [])
    }
    return organized


# Analyze bookmark titles with spaCy
def analyze_bookmarks_with_spacy(bookmarks, nlp_model):
    for bookmark in bookmarks:
        doc = nlp_model(bookmark.get("title", ""))
        bookmark["entities"] = [ent.text for ent in doc.ents]
    return bookmarks


# Extract keywords from text
def extract_keywords(text):
    tokens = word_tokenize(text)
    return [
        word.lower()
        for word in tokens
        if word.isalpha() and word.lower() not in stopwords.words("english")
    ]


# Group bookmarks by keywords
def group_bookmarks(bookmarks):
    folders = defaultdict(list)
    for title, content in bookmarks.items():
        keywords = extract_keywords(content)
        for keyword in keywords:
            folders[keyword].append(title)
    return folders


# Import folders to Notion
def import_to_notion(bookmarks_folders, notion_token, database_id):
    notion = Client(auth=notion_token)
    for folder in bookmarks_folders:
        notion.pages.create(
            parent={"database_id": database_id},
            properties={"Name": {"title": [{"text": {"content": folder}}]}},
        )


# Main function to process bookmarks
def main():
    # User inputs
    bookmarks_path = input("Enter the path to your bookmarks file: ")
    notion_token = input("Enter your Notion integration token: ")
    database_id = input("Enter your Notion database ID: ")

    # Load bookmarks
    bookmarks_data = load_bookmarks(bookmarks_path)
    if not bookmarks_data:
        return

    # Organize and display bookmarks
    organized_bookmarks = organize_bookmarks(bookmarks_data)
    for folder, bookmarks in organized_bookmarks.items():
        print(f"Folder: {folder}\nBookmarks: {bookmarks}\n")

    # Extract folder names
    folder_names = extract_folders(
        bookmarks_data.get("roots", {}).get("bookmark_bar", {}).get("children", [])
    )
    print(pd.DataFrame(folder_names, columns=["Folders"]))

    # Import to Notion
    if folder_names:
        import_to_notion(folder_names, notion_token, database_id)


if __name__ == "__main__":
    main()
