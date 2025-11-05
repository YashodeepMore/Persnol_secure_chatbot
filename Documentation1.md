# Offline Message Reader (Phase 1)

## 📖 Overview
This module is the offline foundation for a larger privacy-focused personal data app.  
It reads and processes local SMS and email samples stored as JSON files — no internet or API connection required.

---

## 🧩 Project Structure


project_root/
│
├── sample_messages/
│ ├── sms.json
│ ├── emails.json
│
├── message_reader.py # Functions to read SMS and email data
├── main.py # Entry point (to test functionality)
└── README.md # Project documentation



---

## ⚙️ Features Implemented (So Far)
### ✅ Step 1: Local Data Reading
- **`read_sms(file_path)`**  
  Reads SMS messages from a local JSON file.
  ```python
  def read_sms(file_path: str) -> list:
      """Reads SMS data from JSON file."""


[
    {
        "sender": "Amazon",
        "text": "Hey Yashodeep, your order #4587 will be delivered tomorrow by 5 PM.",
        "timestamp": "2025-10-31T17:00:00"
    },
    ...
]


def read_emails(file_path: str) -> list:
    """Reads Email data from JSON file."""


[
    {
        "from": "hr@xyzcorp.com",
        "subject": "Meeting Reminder",
        "body": "Your project review meeting is scheduled for 2 PM tomorrow (Friday).",
        "date": "2025-10-30T10:00:00"
    },
    ...
]


🧠 Next Steps

Text Preprocessing

Normalize text

Parse timestamps

Clean punctuation and noise

Message Analysis

Categorize message type (transaction/order/reminder)

Extract key info (amount, date, sender)

Gmail API Integration

Fetch real emails securely

Replace local file input with API data

💡 Documentation Guidelines

When documenting future modules:

Add short docstrings to every function (1–2 lines)

Update README.md after each major step

Include examples (input/output snippets)

Use clear headings for each feature

Example docstring style:


def preprocess_text(text: str) -> str:
    """
    Cleans and normalizes text messages.
    Removes unwanted symbols, converts to lowercase, and trims spaces.
    """


