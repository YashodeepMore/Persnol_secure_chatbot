
# 📄 **Clean RAG Message Format (v1)**

This document defines how retrieved messages must be formatted **after masking** and **before sending** to the cloud LLM.
The goal is to remove all noise, logs, timestamps, and irrelevant metadata so that the LLM receives clean, structured content.

---

# 🎯 **1. Purpose**

To convert raw retrieved messages (which may contain logs, timestamps, distances, etc.) into a **clean, minimal, consistent format** that the LLM can understand.

Only the **masked content** of the message should be sent to the cloud.

---

# 🧹 **2. Cleaning Rules**

All retrieved messages must follow these rules:

1. **Remove timestamps**
   (e.g., `[2025-11-15 20:56:06,558]`)

2. **Remove log metadata**
   (`INFO -`, `root -`, `58`, etc.)

3. **Remove distance scores**
   (`Distance: 1.277`)

4. **Remove message type**
   (transaction/general/reminder unless needed for meaning)

5. **Remove blank lines and extra spacing**

6. **Keep only the message text after masking**

7. **Do NOT break text across multiple lines**

8. **Each message must be enclosed in quotes**
   `"<masked_message>"`

9. **Messages must be numbered**
   `1.`, `2.`, `3.`

---

# 🧩 **3. Final RAG Message Format**

```
USER QUERY:
"<user_query>"

RETRIEVED MESSAGES:
1. "<masked_message_1>"
2. "<masked_message_2>"
3. "<masked_message_3>"
```

---

# 📦 **4. Clean Message Example**

### **Raw Retrieved Message (actual FAISS log)**

```
[ 2025-11-15 20:56:06,558 ] 58 root - INFO - 
SMS from Google Pay: Payment of Rs. #amount_1 to #receiver_1 for dinner was successful. Ref ID: #refid_1.
[ 2025-11-15 20:56:06,558 ] 59 root - INFO - Distance: 1.277
```

### **Clean RAG Message**

```
1. "Payment of Rs. #amount_1 to #receiver_1 for dinner was successful. Ref ID: #refid_1."
```

---

# 📦 **5. Full Prompt Example to Cloud LLM**

```
USER QUERY:
"I paid some people, can you calculate total amount?"

RETRIEVED MESSAGES:
1. "Payment of Rs. #amount_1 to #receiver_1 for dinner."
2. "Invoice due: Rs. #amount_2 for raw materials."
3. "Movie tickets confirmed. No payment."
```

---

# 📌 **6. Required Properties**

* Messages must be **short**, **clean**, and **focused on meaning**.
* Masked placeholders such as `#amount_1`, `#receiver_2` must remain untouched.
* No irrelevant noise or metadata should be visible to the cloud LLM.

---

# 🧠 **7. Why This Format Is Important**

This format ensures:

* LLM understands the messages clearly
* Placeholders are preserved
* No personal data leaks
* Prompts remain small and efficient
* Outputs are predictable and stable

