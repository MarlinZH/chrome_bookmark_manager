# legacy 

# import json
# import xmind
# from xmind.core.topic import TopicElement


# def create_xmind_from_google_bookmarks(json_file, xmind_file):
#     # Load the JSON file
#     with open(json_file, 'r', encoding='utf-8') as file:
#         data = json.load(file)

#     # Initialize XMind workbook
#     workbook = xmind.load(xmind_file)
#     sheet = workbook.getPrimarySheet()
#     sheet.setTitle("Google Bookmarks")
#     root_topic = sheet.getRootTopic()
#     root_topic.setTitle("Bookmarks")

#     def add_hierarchy(parent_topic, bookmarks):
#         for bookmark in bookmarks:
#             if 'title' in bookmark:
#                 topic = TopicElement()
#                 topic.setTitle(bookmark['title'])
#                 parent_topic.addSubTopic(topic)

#                 # Recur for subfolders or items if any
#                 if 'children' in bookmark:
#                     add_hierarchy(topic, bookmark['children'])
#             elif 'children' in bookmark:
#                 # Folder with no title, recurse into its children
#                 add_hierarchy(parent_topic, bookmark['children'])

#     # Parse the JSON data into the XMind structure
#     if 'roots' in data and 'bookmark_bar' in data['roots']:
#         add_hierarchy(root_topic, data['roots']['bookmark_bar']['children'])

#     # Save the XMind file
#     xmind.save(workbook, xmind_file)
#     print(f"XMind file '{xmind_file}' created successfully.")


# # Example usage
# google_bookmarks_json = r"C:\Users\FROAP\AppData\Local\Google\Chrome\User Data\Default\Bookmarks" # Path to your Google Bookmarks JSON file
# output_xmind_file = "Google_Bookmarks.xmind"  # Path for the output XMind file

# create_xmind_from_google_bookmarks(google_bookmarks_json, output_xmind_file)


# def create_meta_xml(output_dir):
#     """
#     Generate meta.xml file required for XMind.
#     """
#     meta_xml_content = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
# <meta xmlns="urn:xmind:xmap:xmlns:meta:2.0" version="2.0">
#   <Creator>Python Script</Creator>
# </meta>
# """
#     meta_path = os.path.join(output_dir, "meta.xml")
#     with open(meta_path, "w", encoding="utf-8") as file:
#         file.write(meta_xml_content)


# def create_styles_xml(output_dir):
#     """
#     Generate styles.xml file required for XMind.
#     """
#     styles_xml_content = """<?xml version="1.0" encoding="UTF-8"?>
# <styles xmlns="urn:xmind:xmap:xmlns:style:2.0">
#   <style id="default-topic" type="topic">
#     <topic-properties shape-class="org.xmind.topicShape.roundedRect" />
#   </style>
# </styles>
# """
#     styles_path = os.path.join(output_dir, "styles.xml")
#     with open(styles_path, "w", encoding="utf-8") as file:
#         file.write(styles_xml_content)


# def create_manifest(output_dir):
#     """
#     Generate the META-INF/manifest.xml file required for XMind.
#     """
#     meta_inf_dir = os.path.join(output_dir, "META-INF")
#     os.makedirs(meta_inf_dir, exist_ok=True)
#     manifest_content = """<?xml version="1.0" encoding="UTF-8"?>
# <manifest xmlns="urn:xmind:xmap:xmlns:manifest:1.0">
#   <file-entry full-path="content.xml" media-type="text/xml" />
#   <file-entry full-path="meta.xml" media-type="text/xml" />
#   <file-entry full-path="styles.xml" media-type="text/xml" />
# </manifest>
# """
#     manifest_path = os.path.join(meta_inf_dir, "manifest.xml")
#     with open(manifest_path, "w", encoding="utf-8") as file:
#         file.write(manifest_content)


# def parse_bookmarks(bookmarks, parent=None):
#     """
#     Recursively parses Google Bookmarks JSON data into a hierarchy suitable for XMind.
#     """
#     topics = []
#     for bookmark in bookmarks:
#         # Debugging: Print the structure to verify
#         print(f"Processing: {bookmark}")
#         if isinstance(bookmark, dict) and "children" in bookmark:  # It's a folder
#             topic = {
#                 "id": str(uuid.uuid4()),
#                 "title": bookmark.get("name", "Untitled Folder"),
#                 "children": {
#                     "attached": parse_bookmarks(
#                         bookmark["children"], parent=bookmark.get("id", None)
#                     )
#                 },
#             }
#         elif isinstance(bookmark, dict) and "name" in bookmark:  # It's a bookmark
#             topic = {
#                 "id": str(uuid.uuid4()),
#                 "title": bookmark.get("name", "Untitled Bookmark"),
#             }
#         else:
#             raise ValueError(f"Unexpected bookmark structure: {bookmark}")
#         topics.append(topic)
#     return topics


# def generate_content_xml(bookmarks_json, output_dir):
#     """
#     Generate content.xml file for XMind.
#     """
#     content_xml_path = os.path.join(output_dir, "content.xml")

#     # Root topic
#     root_topic = {
#         "id": "root-topic",
#         "title": "Google Bookmarks",
#         "children": {"attached": parse_bookmarks(bookmarks_json)},
#     }

#     # Create XML content
#     xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
#     xml_content += '<xmap-content xmlns="urn:xmind:xmap:xmlns:content:2.0">\n'
#     xml_content += '  <sheet id="sheet-1" class="sheet">\n'
#     xml_content += "    <title>Google Bookmarks</title>\n"
#     xml_content += f'    <topic id="{root_topic["id"]}">\n'
#     xml_content += f'      <title>{root_topic["title"]}</title>\n'

#     def add_children(children, indent=6):
#         xml = ""
#         for child in children:
#             child_title = child.get("title", "")
#             child_id = child["id"]
#             xml += " " * indent + f'<topic id="{child_id}">\n'
#             xml += " " * (indent + 2) + f"<title>{child_title}</title>\n"
#             if "children" in child:
#                 xml += add_children(child["children"]["attached"], indent + 4)
#             xml += " " * indent + "</topic>\n"
#         return xml

#     xml_content += add_children(root_topic["children"]["attached"])
#     xml_content += "    </topic>\n"
#     xml_content += "  </sheet>\n"
#     xml_content += "</xmap-content>\n"

#     # Write to content.xml
#     os.makedirs(output_dir, exist_ok=True)
#     with open(content_xml_path, "w", encoding="utf-8") as file:
#         file.write(xml_content)


# def rezip_as_xmind(source_dir, output_xmind_file):
#     """
#     Re-zips a folder into an XMind file.
#     """
#     with zipfile.ZipFile(output_xmind_file, "w", zipfile.ZIP_DEFLATED) as zipf:
#         for root, _, files in os.walk(source_dir):
#             for file in files:
#                 file_path = os.path.join(root, file)
#                 arcname = os.path.relpath(file_path, start=source_dir)
#                 zipf.write(file_path, arcname)
#     print(f"XMind file created at {output_xmind_file}")


# # Example usage
# google_bookmarks_json = r"C:\Users\FROAP\AppData\Local\Google\Chrome\User Data\Default\Bookmarks"  # Path to your Google Bookmarks JSON file

# output_directory = "xmind_structure"
# xmind_output_file = "bookmarks.xmind"

# # Generate XMind components
# generate_content_xml(google_bookmarks_json, output_directory)
# create_meta_xml(output_directory)
# create_styles_xml(output_directory)
# create_manifest(output_directory)

# # Re-zip as XMind
# rezip_as_xmind(output_directory, xmind_output_file)

import os
import json
import uuid
import zipfile


def parse_chrome_bookmarks(bookmarks, parent=None):
    """
    Recursively parse Chrome bookmarks into a hierarchy suitable for XMind.
    """
    topics = []
    for item in bookmarks:
        if item["type"] == "folder":
            topic = {
                "id": str(uuid.uuid4()),
                "title": item.get("name", "Untitled Folder"),
                "children": {
                    "attached": parse_chrome_bookmarks(
                        item.get("children", []), parent=item.get("id")
                    )
                },
            }
        elif item["type"] == "url":
            topic = {
                "id": str(uuid.uuid4()),
                "title": item.get("name", "Untitled Bookmark"),
                "notes": item.get("url", ""),
            }
        else:
            continue  # Skip unsupported types
        topics.append(topic)
    return topics


def generate_content_files(chrome_bookmarks_json, output_directory):
    """
    Generate content.xml and content.json for an XMind file based on Chrome Bookmarks JSON.
    """
    # Load the JSON file with UTF-8 encoding
    with open(chrome_bookmarks_json, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Access the bookmark_bar -> children section
    bookmarks_data = data["roots"]["bookmark_bar"]["children"]

    # Parse the bookmarks into XMind structure
    parsed_bookmarks = parse_chrome_bookmarks(bookmarks_data)

    # XMind content structure
    xmind_content = {
        "version": "2.0",
        "topic": {
            "id": str(uuid.uuid4()),
            "title": "Chrome Bookmarks",
            "children": {"attached": parsed_bookmarks},
        },
    }

    # Generate content.xml
    content_xml_path = os.path.join(output_directory, "content.xml")
    with open(content_xml_path, "w", encoding="utf-8") as xml_file:
        xml_file.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            + json.dumps(xmind_content, indent=2)
        )
    print(f"Generated: {content_xml_path}")

    # Generate content.json
    content_json_path = os.path.join(output_directory, "content.json")
    with open(content_json_path, "w", encoding="utf-8") as json_file:
        json.dump(xmind_content, json_file, indent=2)
    print(f"Generated: {content_json_path}")


def create_xmind_archive(output_directory, output_xmind_file):
    """
    Package the folder into an XMind file.
    """
    with zipfile.ZipFile(output_xmind_file, "w", zipfile.ZIP_DEFLATED) as xmind_file:
        for foldername, subfolders, filenames in os.walk(output_directory):
            for filename in filenames:
                filepath = os.path.join(foldername, filename)
                arcname = os.path.relpath(filepath, output_directory)
                xmind_file.write(filepath, arcname)
    print(f"XMind file created: {output_xmind_file}")


def main():
    # Input Chrome Bookmarks JSON file
    chrome_bookmarks_json =  (
        r"C:\Users\FROAP\AppData\Local\Google\Chrome\User Data\Default\Bookmarks"  # Path to your Google Bookmarks JSON file
    )

    # Output directory for XMind content files
    output_directory = r"C:\Users\Froap\_DEV\chrome_bookmark_Management\unzipped_xmind"
    os.makedirs(output_directory, exist_ok=True)

    # Generate content.xml
    generate_content_files(chrome_bookmarks_json, output_directory)

    # Additional required files for XMind
    with open(
        os.path.join(output_directory, "meta.xml"), "w", encoding="utf-8"
    ) as file:
        file.write('<?xml version="1.0" encoding="UTF-8"?><meta version="2.0"/>')

    with open(
        os.path.join(output_directory, "styles.xml"), "w", encoding="utf-8"
    ) as file:
        file.write('<?xml version="1.0" encoding="UTF-8"?><xmap-styles version="2.0"/>')

    # Create the XMind file
    output_xmind_file = "output.xmind"
    create_xmind_archive(output_directory, output_xmind_file)


if __name__ == "__main__":
    main()
