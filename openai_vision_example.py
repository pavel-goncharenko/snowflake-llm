"""
https://docs.snowflake.com/en/user-guide/snowflake-cortex/open_ai_sdk
"""

import os
import base64
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


client = OpenAI(
  api_key=os.getenv("SNOWFLAKE_PAT"),
  base_url=f"https://{os.getenv('SNOWFLAKE_ACCOUNT')}.snowflakecomputing.com/api/v2/cortex/v1"
)

# Read and encode the image
image_path = os.path.join(os.path.dirname(__file__), "images", "REAL_ESTATE_STAGING.png")
with open(image_path, "rb") as image_file:
    image_data = base64.b64encode(image_file.read()).decode('utf-8')

response = client.chat.completions.create(
  model="openai-gpt-5-mini",
  messages=[
    {
      "role": "user",
      "content": [
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/png;base64,{image_data}"
          }
        },
        {
          "type": "text",
          "text": "Determine most related room types from the list (Living Area, Kitchen, Bath, Garden, Master Bedroom) to the given image. Respond in JSON without markdown. Example: {\"labels\": [\"A\"]}"
        }
      ]
    }
  ],
)

print(response.choices[0].message.content)
