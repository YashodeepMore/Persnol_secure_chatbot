## 🧩 Step 2: Preprocess and Analyze Messages

**Goal:** Extract useful structured information from the raw message text.

**Why:**
Before integrating with external APIs (like Gmail or SMS), it's best to build a **message understanding pipeline**. This ensures your application can consistently interpret any input, regardless of whether it's local data or API-based.

---

### 🧠 Step 2A: Text Preprocessing

This step focuses on **cleaning and normalizing** the text to prepare it for analysis.

* **Remove/Normalize Unwanted Characters:** Fix inconsistencies like removing periods from abbreviations (e.g., "Rs." $\to$ "**Rs**").
* **Convert Timestamps:** Transform raw timestamp strings into **Python `datetime`** objects for easy manipulation and comparison.
* **Lowercase Normalization:** Convert all text to **lowercase** to ensure consistency and improve pattern matching.

---

### 🧾 Step 2B: Basic Classification

This step involves extracting high-level information and entities from the preprocessed text.

* **Type Detection:** Identify the core category of the message, such as:
    * **transaction**
    * **order**
    * **reminder**
    * **offer**
    * *etc.*
* **Entity Extraction:** Pull out specific, valuable pieces of data:
    * **amounts**
    * **names**
    * **dates/times**
    * *etc.*

| Example Input | Detected Type | Extracted Entities |
| :--- | :--- | :--- |
| SMS from HDFC: "A/C credited with Rs 1200" | **Transaction** | `amount` = **1200** |
| Email from "xyzcorp": "Meeting tomorrow at 2 PM" | **Meeting/Reminder** | `time` = **2 PM tomorrow** |

---

### 🧰 Implementation Order

We will build the message processing logic in the following sequence:

1.  `preprocess_text()`: Handles cleaning and normalization.
2.  `analyze_sms(messages)`: Implements analysis for pattern-based data (e.g., bank transactions, orders).
3.  `analyze_email(emails)`: Extracts information from less structured email bodies (e.g., reminders, offers, flight details).

---

## 🚀 Step 3 (later)

Once the message analysis works robustly with offline (local JSON) data, the next step will be to **connect to the Gmail API** and replace the local input with real-time emails.