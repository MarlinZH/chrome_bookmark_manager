def organize_bookmarks(bookmarks_data):
    # Access the "bookmark_bar"
    bookmark_bar = bookmarks_data.get("roots", {}).get("bookmark_bar", {})

    # Initialize a dictionary to store bookmarks organized by folders
    organized_bookmarks = {}

    # Iterate through folders
    for folder in bookmark_bar.get("children", []):
        folder_name = folder.get("name", "")
        folder_bookmarks = folder.get("children", [])

        # Create an entry for the folder in the organized dictionary
        organized_bookmarks[folder_name] = []

        # Iterate through bookmarks within the folder
        for bookmark in folder_bookmarks:
            bookmark_name = bookmark.get("name", "")
            organized_bookmarks[folder_name].append(bookmark_name)

    return organized_bookmarks


# Example usage:
bookmarks_data = {...}  # Replace with your actual JSON data
organized_bookmarks = organize_bookmarks(bookmarks_data)

# Print the organized bookmarks
for folder, bookmarks in organized_bookmarks.items():
    print(f"Folder: {folder}")
    print(f"Bookmarks: {bookmarks}")
    print()

# Assuming 'bookmarks_data' contains your JSON data

# Access the folders within the "bookmark_bar"
bookmark_bar = bookmarks_data.get("roots", {}).get("bookmark_bar", {})
folders = bookmark_bar.get("children", [])

# Extract folder names
folder_names = [folder.get("name", "") for folder in folders]

# Print the folder names
print(folder_names)

import spacy
import json


def analyze_bookmarks_with_spacy(bookmarks):
    # Load spaCy English model
    nlp = spacy.load("en_core_web_sm")

    # Process each bookmark
    for bookmark in bookmarks:
        title = bookmark["title"]

        # Analyze the title using spaCy
        doc = nlp(title)

        # Extract entities, keywords, or other relevant information
        entities = [ent.text for ent in doc.ents]

        # Update the bookmark with additional analysis results
        bookmark["entities"] = entities

    return bookmarks


def main():
    # Replace 'path_to_bookmarks.json' with the actual path to your JSON file
    with open("path_to_bookmarks.json", "r", encoding="utf-8") as file:
        bookmarks = json.load(file)

    # Analyze bookmarks with spaCy
    analyzed_bookmarks = analyze_bookmarks_with_spacy(bookmarks)

    # Print the analyzed bookmarks
    print(json.dumps(analyzed_bookmarks, indent=2))


if __name__ == "__main__":
    main()


import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
import os

# Sample bookmarks
bookmarks = {
    "Bookmark 1": "Article about machine learning techniques",
    "Bookmark 2": "Python tutorial for data analysis",
    "Bookmark 3": "Recipe for chocolate cake",
    # Add more bookmarks here
}

# NLTK setup
nltk.download("punkt")
nltk.download("stopwords")


# Function to extract keywords
def extract_keywords(text):
    tokens = word_tokenize(text)
    keywords = [
        word.lower()
        for word in tokens
        if word.isalpha() and word.lower() not in stopwords.words("english")
    ]
    return keywords


# Function to group bookmarks into folders
def group_bookmarks(bookmarks):
    folders = defaultdict(list)
    for title, content in bookmarks.items():
        keywords = extract_keywords(content)
        for keyword in keywords:
            folders[keyword].append(title)
    return folders


# Create folders and move bookmarks
def create_folders_and_move_bookmarks(bookmarks):
    folders = group_bookmarks(bookmarks)
    for topic, bookmark_titles in folders.items():
        folder_name = topic.replace(" ", "_")
        os.makedirs(folder_name, exist_ok=True)
        for bookmark_title in bookmark_titles:
            # Move the bookmark file to the folder
            # Example code to move file: shutil.move(source, destination)
            print(f"Moved {bookmark_title} to {folder_name}")


# Example usage
create_folders_and_move_bookmarks(bookmarks)
def organize_bookmarks(bookmarks_data):
    # Access the "bookmark_bar"
    bookmark_bar = bookmarks_data.get("roots", {}).get("bookmark_bar", {})

    # Initialize a dictionary to store bookmarks organized by folders
    organized_bookmarks = {}

    # Iterate through folders
    for folder in bookmark_bar.get("children", []):
        folder_name = folder.get("name", "")
        folder_bookmarks = folder.get("children", [])

        # Create an entry for the folder in the organized dictionary
        organized_bookmarks[folder_name] = []

        # Iterate through bookmarks within the folder
        for bookmark in folder_bookmarks:
            bookmark_name = bookmark.get("name", "")
            organized_bookmarks[folder_name].append(bookmark_name)

    return organized_bookmarks


# Example usage:
bookmarks_data = {...}  # Replace with your actual JSON data
organized_bookmarks = organize_bookmarks(bookmarks_data)

# Print the organized bookmarks
for folder, bookmarks in organized_bookmarks.items():
    print(f"Folder: {folder}")
    print(f"Bookmarks: {bookmarks}")
    print()

import json
import pandas as pd
from notion_client import Client


def load_bookmarks(bookmarks_path):
    try:
        with open(bookmarks_path, "r", encoding="utf-8") as file:
            bookmarks_content = json.load(file)
        return bookmarks_content
    except FileNotFoundError:
        print(f"Error: File not found at {bookmarks_path}")
        return None
    except json.JSONDecodeError:
        print("Error: File is not a valid JSON.")
        return None


def extract_folders(children, bookmarks_folders):
    for child in children:
        if child["type"] == "folder":
            bookmarks_folders.append(child["name"])
            if "children" in child:
                extract_folders(child["children"], bookmarks_folders)


def identify_folders(bookmarks_path):
    bookmarks_content = load_bookmarks(bookmarks_path)
    if not bookmarks_content:
        return
    bookmarks_root = bookmarks_content["roots"]
    bookmark_bar = bookmarks_root["bookmark_bar"]
    bookmark_bar_children = bookmark_bar["children"]
    bookmarks_folders = []
    extract_folders(bookmark_bar_children, bookmarks_folders)
    df = pd.DataFrame(bookmarks_folders, columns=["Folders"])
    print(df)
    return bookmarks_folders


def import_to_notion(bookmarks_folders, notion_token, database_id):
    notion = Client(auth=notion_token)
    for folder in bookmarks_folders:
        notion.pages.create(
            parent={"database_id": database_id},
            properties={"Name": {"title": [{"text": {"content": folder}}]}},
        )


def main():
    bookmarks_path = (
        r"C:\Users\FROAP\AppData\Local\Google\Chrome\User Data\Default\Bookmarks"
    )
    notion_token = "your_notion_integration_token"
    database_id = "your_notion_database_id"
    bookmarks_folders = identify_folders(bookmarks_path)
    if bookmarks_folders:
        import_to_notion(bookmarks_folders, notion_token, database_id)


if __name__ == "__main__":
    main()

import json
import pandas as pd


def load_bookmarks(bookmarks_path):
    try:
        with open(bookmarks_path, "r", encoding="utf-8") as file:
            bookmarks_content = json.load(file)
        return bookmarks_content
    except FileNotFoundError:
        print(f"Error: File not found at {bookmarks_path}")
        return None
    except json.JSONDecodeError:
        print("Error: File is not a valid JSON.")
        return None


def extract_folders(children, bookmarks_folders):
    for child in children:
        if child["type"] == "folder":
            bookmarks_folders.append(child["name"])
            if "children" in child:
                extract_folders(child["children"], bookmarks_folders)


def identify_folders(bookmarks_path):
    bookmarks_content = load_bookmarks(bookmarks_path)
    if not bookmarks_content:
        return
    bookmarks_root = bookmarks_content["roots"]
    bookmark_bar = bookmarks_root["bookmark_bar"]
    bookmark_bar_children = bookmark_bar["children"]
    bookmarks_folders = []
    extract_folders(bookmark_bar_children, bookmarks_folders)
    df = pd.DataFrame(bookmarks_folders, columns=["Folders"])
    print(df)


def main():
    bookmarks_path = input("Enter the path to your Chrome Bookmarks file: ")
    identify_folders(bookmarks_path)


if __name__ == "__main__":
    main()

import json
import pandas as pd
from notion_client import Client


def load_bookmarks(bookmarks_path):
    try:
        with open(bookmarks_path, "r", encoding="utf-8") as file:
            bookmarks_content = json.load(file)
        return bookmarks_content
    except FileNotFoundError:
        print(f"Error: File not found at {bookmarks_path}")
        return None
    except json.JSONDecodeError:
        print("Error: File is not a valid JSON.")
        return None


def extract_folders(children, bookmarks_folders):
    for child in children:
        if child["type"] == "folder":
            bookmarks_folders.append(child["name"])
            if "children" in child:
                extract_folders(child["children"], bookmarks_folders)


def identify_folders(bookmarks_path):
    bookmarks_content = load_bookmarks(bookmarks_path)
    if not bookmarks_content:
        return
    bookmarks_root = bookmarks_content["roots"]
    bookmark_bar = bookmarks_root["bookmark_bar"]
    bookmark_bar_children = bookmark_bar["children"]
    bookmarks_folders = []
    extract_folders(bookmark_bar_children, bookmarks_folders)
    df = pd.DataFrame(bookmarks_folders, columns=["Folders"])
    print(df)
    return bookmarks_folders


def import_to_notion(bookmarks_folders, notion_token, database_id):
    notion = Client(auth=notion_token)
    for folder in bookmarks_folders:
        notion.pages.create(
            parent={"database_id": database_id},
            properties={"Name": {"title": [{"text": {"content": folder}}]}},
        )


def main():
    bookmarks_path = (
        r"C:\Users\FROAP\AppData\Local\Google\Chrome\User Data\Default\Bookmarks"
    )
    notion_token = "your_notion_integration_token"
    database_id = "your_notion_database_id"
    bookmarks_folders = identify_folders(bookmarks_path)
    if bookmarks_folders:
        import_to_notion(bookmarks_folders, notion_token, database_id)


if __name__ == "__main__":
    main()
