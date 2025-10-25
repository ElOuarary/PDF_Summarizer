from dotenv import load_dotenv
import httpx
import os

load_dotenv()

class Client:
  def __init__(self, notion_token):
    self.notion_token = notion_token
    self.headers = {
      'Authorization': f'Bearer {os.environ.get('NOTION_TOKEN')}',
      'Content-Type': 'application/json',
      'Notion-Version': '2025-09-03'
    }
    self.search_params = {"filter": {"value": "page", "property": "object"}}
    
  def fetch_page_id(self):
    search_response = httpx.post(
      f'https://api.notion.com/v1/search',
      json=self.search_params, headers=self.headers
    )
    return search_response.json()['results'][0]['id']
  
  def create_page(self, content):
    page_id = self.fetch_page_id()
    create_page_body = {
      "parent": {"page_id": page_id },
      "properties": {
        "title": {
          "title": [{ 
            "type": "text", 
            "text": { "content": "Hello World!" }
            }]
        }
      },
      "children": [{
        "object": "block",
        "type": "paragraph",
        "paragraph": {
          "rich_text": [{ 
            "type": "text", 
            "text": { 
              "content": content 
            } 
          }]
        }
      }]
    }
    httpx.post(
       "https://api.notion.com/v1/pages", 
      json=create_page_body, headers=self.headers
    )