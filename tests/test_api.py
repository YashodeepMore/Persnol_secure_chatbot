import requests
import os
from dotenv import load_dotenv

load_dotenv()
url = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://your-site.com",  # optional
    "X-Title": "Your App Name"               # optional
}
content = """
You are a natural-language reasoning assistant for a RAG system.

IMPORTANT RULES:
- The text contains masked entities like #amount, #receiver, #date.
- These placeholders MUST remain EXACTLY as they appear.
- NEVER replace, modify, create, or remove placeholders.
- Never hallucinate real names, numbers, dates, or apps.
- Only summarize or compute using the placeholders given.
- Ignore messages that do NOT contain #amount if question is about payments.
- If total cannot be calculated because placeholders are the same, say so.

USER QUERY:
"i paid some people can you calculate total amount"

RETRIEVED MESSAGES:
1. "Payment of Rs. #amount_1 to #receiver_1 for dinner was successful."
2. "Invoice for raw materials. Amount due: Rs. #amount_2."
3. "Movie tickets confirmed. (no payment information)"

TASK:
- Identify which messages represent payments.
- Use only the placeholders to calculate.
- If multiple different #amount placeholders exist, express total as (#amount + #amount).
- If the same placeholder repeats, say: 
  "Both payments use the placeholder #amount, so the total cannot be calculated."

Give final answer in 1–2 sentences.

"""
data = {
    "model": "kwaipilot/kat-coder-pro:free",
    "messages": [
        {"role": "user", "content": content}   
    ]
}

response = requests.post(url, headers=headers, json=data)

data = response.json()

if "choices" in data:
    print(data["choices"][0]["message"]["content"])
else :
    print("error responce : ", data)
