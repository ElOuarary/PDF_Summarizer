import httpx
import logging


class Client:
    def __init__(self, notion_token, notion_page_id):
      self.logger = logging.getLogger(__name__)
      self.notion_token = notion_token
      self.notion_page_id = notion_page_id
      self.headers = {
          'Authorization': f'Bearer {self.notion_token}',
          'Content-Type': 'application/json',
          'Notion-Version': '2025-09-03'
      }
      self.url = 'https://api.notion.com/v1'
    
    def _create_body(self, title, content):
        return {
          "parent": { "page_id": self.notion_page_id },
          "properties": {
            "title": {"title": [{"type": "text", "text": { "content": title}}]}
            },
          "children": [{
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": content}}]}
          }]
        }
        
    
    def create_page(self, title, content):
        body = self._create_body(title, content)
        try:
            responce = httpx.post(self.url+'/pages', json=body, headers=self.headers)
            responce.raise_for_status()
        except Exception as e:
            self.logger.error(f"Failed to create Notion page with content: {e}")
            return None
          
if __name__ == '__main__':
  NOTION_KEY = 'ntn_Z7023538270fR9i7uVziKyPsYM6vrtyhCitzREnySqx4nO'
  client = Client(NOTION_KEY, '2971a2a2-b05e-80da-98f4-e801edaf56fa')
  client.create_page('Testing', 'hello this is my test for configuration')