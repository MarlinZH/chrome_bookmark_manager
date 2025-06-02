class NotionIntegration {
    constructor(token, databaseId) {
        this.token = token;
        this.databaseId = databaseId;
        this.baseUrl = 'https://api.notion.com/v1';
    }

    async createPage(title, properties = {}) {
        const response = await fetch(`${this.baseUrl}/pages`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${this.token}`,
                'Notion-Version': '2022-06-28',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                parent: { database_id: this.databaseId },
                properties: {
                    Name: {
                        title: [
                            {
                                text: {
                                    content: title
                                }
                            }
                        ]
                    },
                    ...properties
                }
            })
        });

        if (!response.ok) {
            throw new Error(`Failed to create Notion page: ${response.statusText}`);
        }

        return await response.json();
    }

    async importBookmarks(bookmarks) {
        const results = [];
        for (const bookmark of bookmarks) {
            try {
                const page = await this.createPage(bookmark.title, {
                    URL: {
                        url: bookmark.url
                    },
                    Folder: {
                        rich_text: [
                            {
                                text: {
                                    content: bookmark.folder || 'Uncategorized'
                                }
                            }
                        ]
                    }
                });
                results.push({ success: true, bookmark, page });
            } catch (error) {
                results.push({ success: false, bookmark, error: error.message });
            }
        }
        return results;
    }
}

export default NotionIntegration; 