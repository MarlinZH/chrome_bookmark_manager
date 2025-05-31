import json
import pandas as pd
from notion_client import Client
import os

def load_env():
    os.environ["NOTION_TOKEN"] = blub.get_secret("NOTION_TOKEN")

    os.environ["DATABASE_ID"] = blub.get_secret("DATABASE_ID")


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

def identify_folders(bookmarks_path):
    bookmarks_content = load_bookmarks(bookmarks_path)
    if not bookmarks_content:
        return
    bookmarks_root = bookmarks_content['roots']
    bookmark_bar = bookmarks_root['bookmark_bar']
    bookmark_bar_children = bookmark_bar['children']
    bookmarks_folders = []
    extract_folders(bookmark_bar_children, bookmarks_folders)
    df = pd.DataFrame(bookmarks_folders, columns=['Folders'])
    print(df)
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
    bookmarks_path = r"C:\Users\FROAP\AppData\Local\Google\Chrome\User Data\Default\Bookmarks"
    bookmark_content = load_bookmarks(bookmarks_path)
    print(bookmark_content)
    bookmark_bar = bookmark_content['roots']['bookmark_bar']['children']
    print(bookmark_bar)
    notion_token = "your_notion_integration_token"
    # database_id = "your_notion_database_id"
    # bookmarks_folders = identify_folders(bookmarks_path)
    # if bookmarks_folders:
    #     import_to_notion(bookmarks_folders, notion_token, database_id)

if __name__ == "__main__":
    main()
