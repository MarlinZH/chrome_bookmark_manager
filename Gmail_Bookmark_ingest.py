import spacy
import json


def get_bookmarks(bookmarks_path):
    with open(bookmarks_path,"r",encoding='utf-8') as file:
        bookmarks_list = json.load(file)
        # print(bookmarks)
        print(json.dumps(bookmarks_list,indent=1))
        return bookmarks_list

# def organize_bookmarks(rows):
#     bookmarks_dict = {}
#     for row in rows:
#         bookmark_id, parent_id, title, url = row
#         bookmark = {'title': title, 'url': url, 'children': []}
#
#         # Check if the parent_id is None (top-level bookmark)
#         if parent_id is None:
#             bookmarks_dict[bookmark_id] = bookmark
#         else:
#             # Add bookmark as a child to its parent
#             bookmarks_dict[parent_id]['children'].append(bookmark)
#
#     # Return top-level bookmarks
#     return list(bookmarks_dict.values())
def analyze_bookmarks(bookmark_list):
    nlp = spacy.load("en_core_web_sm")
    for bookmark in bookmark_list['roots']['bookmark_bar']['children']:
        title = bookmark.get('name', '')
        # print(title)
        doc = nlp(title)
        print(doc)


def main():

    bookmarks_path = "C:\\Users\\FROAP\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Bookmarks"

    bookmarks = get_bookmarks(bookmarks_path)
    analyzer = analyze_bookmarks(bookmarks)

if __name__ == "__main__":
     main()