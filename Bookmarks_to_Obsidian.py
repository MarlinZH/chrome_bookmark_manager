import os
import re
from bs4 import BeautifulSoup

# Configuration
BOOKMARKS_HTML_FILE = "path/to/google_bookmarks.html"  # Replace with the path to your exported HTML file
OBSIDIAN_VAULT_DIR = "path/to/obsidian_vault"  # Replace with the path to your Obsidian vault
OUTPUT_FOLDER = "Google Bookmarks"  # Folder inside the vault to store the bookmarks

# Ensure the output folder exists
output_path = os.path.join(OBSIDIAN_VAULT_DIR, OUTPUT_FOLDER)
os.makedirs(output_path, exist_ok=True)

def parse_bookmarks(html_file):
    """Parse the Google Bookmarks HTML file and extract bookmarks."""
    with open(html_file, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    bookmarks = []
    for tag in soup.find_all("a"):
        title = tag.text.strip()
        url = tag.get("href")
        add_date = tag.get("add_date")
        description = tag.get("description") or ""

        bookmarks.append({
            "title": title,
            "url": url,
            "add_date": add_date,
            "description": description
        })

    return bookmarks

def sanitize_filename(filename):
    """Sanitize the filename to remove invalid characters."""
    return re.sub(r'[\\/*?\"<>|]', "_", filename)

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
    bookmarks = parse_bookmarks(BOOKMARKS_HTML_FILE)
    for bookmark in bookmarks:
        create_markdown_file(bookmark, output_path)

    print(f"Imported {len(bookmarks)} bookmarks into {output_path}")

if __name__ == "__main__":
    main()
