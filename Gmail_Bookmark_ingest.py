import spacy
import json

def load_bookmarks(bookmarks_path):
    with open(bookmarks_path,"r",encoding='utf-8') as file:
        bookmarks_content = json.load(file)
        return bookmarks_content

def analyze_bookmarks(bookmark_list):
    # nlp = spacy.load("en_core_web_sm")
    # for bookmark in bookmark_list['roots']['bookmark_bar']['children']:
    #     title = bookmark_list.get('name', '')
    #     # print(title)
    #     doc = nlp(title)
    #     print(doc)
    for bookmark in bookmark_list['roots']:
        print(bookmark)
        for book in bookmark[0]:
            print(book)


def organize_bookmarks():
    bookmarks_dict = {}
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



def main():
    bookmarks_path = "C:\\Users\\FROAP\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Bookmarks"
    bookmarks = load_bookmarks(bookmarks_path)
    # analyzer = analyze_bookmarks(bookmarks)
    print(json.dumps(bookmarks, indent=1))
if __name__ == "__main__":
     main()