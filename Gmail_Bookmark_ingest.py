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

def main():
    bookmarks_path = r"C:\Users\FROAP\AppData\Local\Google\Chrome\User Data\Default\Bookmarks"
    identify_folders(bookmarks_path)

if __name__ == "__main__":
    main()
