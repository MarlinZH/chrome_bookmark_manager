import spacy
import json
import pandas as pd

def load_bookmarks(bookmarks_path):
    with open(bookmarks_path,"r",encoding='utf-8') as file:
        bookmarks_content = json.load(file)
        return bookmarks_content
    
#READ ROOT LEVEL OF FILE
def identify_folders(bookmarks_path):
    bookmarks_content = load_bookmarks(bookmarks_path)

    # print(bookmarks_content)
    bookmarks_root = bookmarks_content['roots']
    bookmark_bar = bookmarks_root['bookmark_bar']
    bookmark_bar_children = bookmark_bar['children']
    bookmarks_folders = []
    for child in bookmark_bar_children:
        if child['type'] == 'folder' :
            bookmark_folder = child['name']
            bookmarks_folders.append(bookmark_folder)
            bookmark_folder_id = child['guid']
            bookmark_last_used = child['date_last_used']
            if 'children' in bookmark_bar_children:
                for children in child['children']:
                   nested_child = children['name']
            print(child['name'])



    print("ROOT:",bookmarks_root)




 



# def analyze_bookmarks(bookmark_content):
#     for bookmark in bookmark_folders:
#         print(bookmark['name'])
#         # nlp = spacy.load("en_core_web_sm")
#         # for bookmark in bookmark_list['roots']['bookmark_bar']['children']:
#         #     title = bookmark_list.get('name', '')
#         #     # print(title)
#         #     doc = nlp(title)
#         #     print(doc)
#     #     for book in bookmark[0]:
#     #         print(book)
#     return bookmark_bar,bookmarks_list,bookmark


# def organize_bookmarks(bookmark_list):
#     bookmarks_dict = {}


def main():
    bookmarks_path = r"C:\Users\FROAP\AppData\Local\Google\Chrome\User Data\Default\Bookmarks"
    # bookmarks_content = load_bookmarks(bookmarks_path)
    # print(bookmark_file)
    bookmarks_root = identify_folders(bookmarks_path)
    # print(bookmarks_root)
    # folders = identify_folders(bookmarks_content)
    # print(folders)
    # analyzer = analyze_bookmarks(bookmarks)
    # organizer = organize_bookmarks(analyzer)
    # print(organizer)
    # print(json.dumps(bookmarks, indent=1))
if __name__ == "__main__":
     main()
