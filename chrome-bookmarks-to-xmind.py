import json
import os
import xmind
from datetime import datetime
import sys

def get_chrome_bookmarks_path():
    """Get the path to Chrome bookmarks file based on OS"""
    if sys.platform == "win32":
        return os.path.join(os.environ['LOCALAPPDATA'],
                          'Google/Chrome/User Data/Default/Bookmarks')
    elif sys.platform == "darwin":
        return os.path.expanduser(
            '~/Library/Application Support/Google/Chrome/Default/Bookmarks')
    else:  # Linux
        return os.path.expanduser(
            '~/.config/google-chrome/Default/Bookmarks')

def process_bookmark_node(node, topic):
    """Recursively process bookmark nodes and add them to the mind map"""
    if node.get('type') == 'folder':
        # Create a new subtopic for the folder
        subtopic = topic.addSubTopic()
        subtopic.setTitle(node['name'])
        
        # Process children
        for child in node.get('children', []):
            process_bookmark_node(child, subtopic)
    
    elif node.get('type') == 'url':
        # Add URL as a subtopic with hyperlink
        url_topic = topic.addSubTopic()
        url_topic.setTitle(node['name'])
        url_topic.setURLHyperlink(node['url'])

def main():
    try:
        # Get bookmarks file path
        bookmarks_path = get_chrome_bookmarks_path()
        
        if not os.path.exists(bookmarks_path):
            print(f"Error: Chrome bookmarks file not found at {bookmarks_path}")
            return
        
        # Read bookmarks file
        with open(bookmarks_path, 'r', encoding='utf-8') as f:
            bookmarks_data = json.load(f)
        
        # Create new workbook and sheet
        workbook = xmind.load(None)  # Create new workbook
        sheet = workbook.getPrimarySheet()
        root_topic = sheet.getRootTopic()
        root_topic.setTitle("Chrome Bookmarks")
        
        # Process bookmark bar and other bookmarks
        bookmark_bar = bookmarks_data['roots']['bookmark_bar']
        other_bookmarks = bookmarks_data['roots']['other']
        
        # Create main branches
        bookmark_bar_topic = root_topic.addSubTopic()
        bookmark_bar_topic.setTitle("Bookmark Bar")
        
        other_bookmarks_topic = root_topic.addSubTopic()
        other_bookmarks_topic.setTitle("Other Bookmarks")
        
        # Process both main sections
        for child in bookmark_bar.get('children', []):
            process_bookmark_node(child, bookmark_bar_topic)
            
        for child in other_bookmarks.get('children', []):
            process_bookmark_node(child, other_bookmarks_topic)
        
        # Generate output filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"chrome_bookmarks_{timestamp}.xmind"
        
        # Save the mind map
        xmind.save(workbook, output_file)
        print(f"Mind map successfully created: {output_file}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
