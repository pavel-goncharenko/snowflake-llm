"""
Cortex Analyst REST API Client: https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst/rest-api#send-message
"""
from typing import Dict, Any, Optional
import requests


class CortexAnalystClient:
    """Client for working with Cortex Analyst REST API"""

    def __init__(self, account: str, user: str, pat: str):
        """
        Initialize client
        
        Args:
            account: Snowflake account (e.g., abc12345.us-east-1)
            user: Username
            password: Password or token
        """
        self.account = account
        self.user = user
        self.pat = pat
        self.base_url = f"https://{account}.snowflakecomputing.com"
        self.session = requests.Session()

    def send_message(
        self,
        question: str,
        semantic_view: str,
        stream: bool = False
    ) -> Dict[str, Any]:
        """
        Send question to Cortex Analyst
        
        Args:
            question: Question in natural language
            semantic_view: Fully qualified semantic view name (e.g., DB.SCHEMA.VIEW)
            stream: Use streaming mode
            
        Returns:
            Dict: API response
        """

        api_url = f"{self.base_url}/api/v2/cortex/analyst/message"

        request_body = {
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": question
                        }
                    ]
                }
            ],
            "semantic_view": semantic_view,
            "stream": stream
        }

        headers = {
            "Authorization": f"Bearer {self.pat}",
            "Content-Type": "application/json",
            "X-Snowflake-Authorization-Token-Type": "PROGRAMMATIC_ACCESS_TOKEN",
            "Accept": "application/json"
        }

        response = self.session.post(
            api_url,
            json=request_body,
            headers=headers
        )

        # Debug: print response details on error
        if response.status_code >= 400:
            try:
                error_data = response.json()
                raise ValueError(f"API Error {response.status_code}: {error_data}")
            except Exception as e:
                raise ValueError(f"API Error {response.status_code}: {response.text}") from e

        response.raise_for_status()

        return response.json()

    def extract_sql(self, response: Dict[str, Any]) -> Optional[str]:
        """
        Extract SQL from API response
        
        Args:
            response: API response
            
        Returns:
            Optional[str]: SQL query or None
        """
        if 'message' in response and 'content' in response['message']:
            for content_block in response['message']['content']:
                if content_block.get('type') == 'sql':
                    return content_block.get('statement')
        return None

    def extract_text(self, response: Dict[str, Any]) -> Optional[str]:
        """
        Extract text response
        
        Args:
            response: API response
            
        Returns:
            Optional[str]: Text response or None
        """
        if 'message' in response and 'content' in response['message']:
            for content_block in response['message']['content']:
                if content_block.get('type') == 'text':
                    return content_block.get('text')
        return None

    def extract_suggestions(self, response: Dict[str, Any]) -> Optional[list]:
        """
        Extract suggestions for ambiguous questions
        
        Args:
            response: API response
            
        Returns:
            Optional[list]: List of suggestions or None
        """
        if 'message' in response and 'content' in response['message']:
            for content_block in response['message']['content']:
                if content_block.get('type') == 'suggestions':
                    return content_block.get('suggestions', [])
        return None
