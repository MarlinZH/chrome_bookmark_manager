import spacy
import json
import pandas as pd


def load_bookmarks(bookmarks_path):
    with open(bookmarks_path,"r",encoding='utf-8') as file:
        bookmarks_content = json.load(file)
        return bookmarks_content

def analyze_bookmarks(bookmark_content):
    bookmarks_list = bookmark_content['roots']
    # print(bookmarks_list)
    bookmark_bar = bookmarks_list['bookmark_bar']
    print(bookmark_bar)
    bookmark_folders = bookmark_bar['children']
    print(bookmark_folders)
    for bookmark in bookmark_folders:
        print(bookmark['name'])
        # nlp = spacy.load("en_core_web_sm")
        # for bookmark in bookmark_list['roots']['bookmark_bar']['children']:
        #     title = bookmark_list.get('name', '')
        #     # print(title)
        #     doc = nlp(title)
        #     print(doc)
    #     for book in bookmark[0]:
    #         print(book)
    return bookmark_bar,bookmarks_list,bookmark


def organize_bookmarks(bookmark_list):
    bookmarks_dict = {}



def main():
    bookmarks_path = "C:\\Users\\FROAP\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Bookmarks"
    bookmarks = load_bookmarks(bookmarks_path)
    analyzer = analyze_bookmarks(bookmarks)
    organizer = organize_bookmarks(analyzer)
    print(organizer)
    # print(json.dumps(bookmarks, indent=1))
if __name__ == "__main__":
     main()