import json
import pandas as pd
from notion_client import Client
import os
import platform


def get_bookmarks_path():
    system = platform.system()
    if system == "Windows":
        user = os.getlogin()
        return fr"C:\Users\{user}\AppData\Local\Google\Chrome\User Data\Default\Bookmarks"
    elif system == "Linux":
        user = os.getlogin()
        return f"/home/{user}/.config/google-chrome/Default/Bookmarks"
    elif system == "Darwin":
        user = os.getlogin()
        return f"/Users/{user}/Library/Application Support/Google/Chrome/Default/Bookmarks"
    else:
        raise Exception("Unsupported OS")


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
        if child['type'] == 'folder':
            bookmarks_folders.append(child['name'])
            if 'children' in child:
                extract_folders(child['children'], bookmarks_folders)


def identify_folders(bookmarks_content):
    bookmarks_root = bookmarks_content['roots']
    bookmark_bar = bookmarks_root['bookmark_bar']
    bookmark_bar_children = bookmark_bar['children']
    bookmarks_folders = []
    extract_folders(bookmark_bar_children, bookmarks_folders)
    return bookmarks_folders


def import_to_notion(bookmarks_folders, notion_token, database_id):
    notion = Client(auth=notion_token)
    for folder in bookmarks_folders:
        notion.pages.create(
            parent={"database_id": database_id},
            properties={
                "Name": {
                    "title": [
                        {
                            "text": {
                                "content": folder
                            }
                        }
                    ]
                }
            }
        )


def main():
    bookmarks_path = get_bookmarks_path()
    notion_token = os.getenv("NOTION_TOKEN")
    database_id = os.getenv("DATABASE_ID")
    if not notion_token or not database_id:
        print("Please set NOTION_TOKEN and DATABASE_ID environment variables.")
        return
    bookmarks_content = load_bookmarks(bookmarks_path)
    if not bookmarks_content:
        return
    bookmarks_folders = identify_folders(bookmarks_content)
    if bookmarks_folders:
        import_to_notion(bookmarks_folders, notion_token, database_id)
        print("Bookmarks folders imported to Notion.")

if __name__ == "__main__":
    main()
