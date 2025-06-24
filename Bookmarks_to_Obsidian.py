import os
import json
import re

# Configuration
#TODO: Make Dynamic
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

    def extract_bookmarks(bookmark_list, folder_path=""):
        for item in bookmark_list:
            current_path = folder_path
            if "name" in item:
                current_path = os.path.join(folder_path, item["name"])

            if "url" in item:
                bookmarks.append(
                    {
                        "title": item.get("name", "Untitled"),
                        "url": item["url"],
                        "add_date": item.get("date_added"),
                        "description": item.get("meta_description", ""),
                        "folder": current_path,
                    }
                )
            if "children" in item:
                extract_bookmarks(item["children"], current_path)

    extract_bookmarks(data.get("roots", {}).get("bookmark_bar", {}).get("children", []))
    return bookmarks


def sanitize_filename(filename):
    """Sanitize the filename to remove invalid characters."""
    return re.sub(r"[\\/*?\"<>|]", "_", filename)


def create_combined_markdown(bookmarks, output_folder):
    """Create a single Markdown file with all bookmarks organized by folder."""
    file_path = os.path.join(output_folder, "Google_Bookmarks.md")

    folder_structure = {}
    for bookmark in bookmarks:
        folder_path = bookmark["folder"].split(os.sep)
        current_level = folder_structure
        for folder in folder_path:
            current_level = current_level.setdefault(folder, {})
        current_level[bookmark["title"]] = bookmark

    def write_folder_contents(folder_dict, indent_level=0):
        output = []
        for key, value in folder_dict.items():
            if isinstance(value, dict) and "url" not in value:
                output.append(f"{'  ' * indent_level}- [[{key}]]\n")
                output.extend(write_folder_contents(value, indent_level + 1))
            elif isinstance(value, dict):
                output.append(
                    f"{'  ' * indent_level}- [[{value['title']}]]({value['url']})\n"
                )
                if value["description"]:
                    output.append(
                        f"{'  ' * (indent_level + 1)}Description: {value['description']}\n"
                    )
        return output

    with open(file_path, "w", encoding="utf-8") as file:
        file.writelines(write_folder_contents(folder_structure))

    print(f"Bookmarks saved to {file_path}")


def main():
    bookmarks = parse_bookmarks(BOOKMARKS_JSON_FILE)
    create_combined_markdown(bookmarks, output_path)


if __name__ == "__main__":
    main()
