import os
import json
import re

# Configuration
BOOKMARKS_JSON_FILE = r"C:\Users\Froap\AppData\Local\Google\Chrome\User Data\Default\Bookmarks"  # Replace with the path to your exported HTML file
OBSIDIAN_VAULT_DIR = r"C:\Users\Froap\OneDrive\.Diagrams\Obsidian-Mainframe"  # Replace with the path to your Obsidian vault
OUTPUT_FOLDER = "Google Bookmarks"  # Folder inside the vault to store the bookmarks
# Ensure the output folder exists
output_path = os.path.join(OBSIDIAN_VAULT_DIR, OUTPUT_FOLDER)
os.makedirs(output_path, exist_ok=True)


def parse_bookmarks(json_file):
    """Parse the Google Bookmarks JSON file and extract bookmarks."""
    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    bookmarks = []

    def extract_bookmarks(bookmark_list):
        for item in bookmark_list:
            if "url" in item:
                bookmarks.append(
                    {
                        "title": item.get("name", "Untitled"),
                        "url": item["url"],
                        "add_date": item.get("date_added"),
                        "description": item.get("meta_description", ""),
                    }
                )
            if "children" in item:
                extract_bookmarks(item["children"])

    extract_bookmarks(data.get("roots", {}).get("bookmark_bar", {}).get("children", []))
    return bookmarks


def sanitize_filename(filename):
    """Sanitize the filename to remove invalid characters."""
    return re.sub(r"[\\/*?\"<>|]", "_", filename)


def create_markdown_file(bookmark, output_folder):
    """Create a Markdown file for a bookmark."""
    title = sanitize_filename(bookmark["title"] or "Untitled")
    filename = f"{title}.md"
    file_path = os.path.join(output_folder, filename)

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(f"---\n")
        file.write(f"title: {bookmark['title']}\n")
        file.write(f"url: {bookmark['url']}\n")
        if bookmark["add_date"]:
            file.write(f"added: {bookmark['add_date']}\n")
        file.write(f"---\n\n")
        file.write(f"[{bookmark['title']}]({bookmark['url']})\n\n")
        if bookmark["description"]:
            file.write(f"Description: {bookmark['description']}\n")


def main():
    bookmarks = parse_bookmarks(BOOKMARKS_JSON_FILE)
    for bookmark in bookmarks:
        create_markdown_file(bookmark, output_path)

    print(f"Imported {len(bookmarks)} bookmarks into {output_path}")


if __name__ == "__main__":
    main()
