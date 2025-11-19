

#  **Local–Cloud LLM Interface Specification (v1)**

This document defines **how local app will communicate with the cloud LLM**.
It is the “API contract” between this device and the cloud.

---

# 📄 **Local–Cloud LLM Interface Specification (v1)**

This document describes the exact structure, fields, and rules for sending masked data to the cloud LLM and receiving its masked response.

This ensures predictable communication and prevents data leaks.

---

# 🎯 **1. Purpose**

To establish a strict, safe, consistent communication protocol between:

* **Local side** (FAISS retrieval + masking + privacy logic)
* **Cloud side** (LLM reasoning + natural response generation)

The cloud receives **only masked information** and returns a **masked answer**.

---

# 🔄 **2. Data Flow Overview**

```
Local Device:
   - Extract entities
   - Mask messages
   - Build clean RAG prompt
   - Send structured JSON → Cloud LLM

Cloud LLM:
   - Generates masked natural-language response
   - Returns JSON → Local Device

Local Device:
   - Re-fill placeholders
   - Compute totals if needed
   - Output final natural answer
```

---

# 🧩 **3. Outgoing Payload (Local → Cloud)**

Local device sends the following JSON to the cloud LLM API:

```json
{
  "query": "<user_query>",
  "messages": [
    "<masked_message_1>",
    "<masked_message_2>",
    "<masked_message_3>"
  ],
  "prompt_template": "<final_prompt_text_generated_locally>"
}
```

### Rules:

* All messages must be **masked**.
* Messages must follow the **clean RAG format**.
* `prompt_template` contains the **entire prompt** including instructions, rules, and the inserted query + messages.

### Important:

* **Never send entity maps.**
* **Never send real values.**
* **Never send logs/distances/files.**

Only clean, masked content.

---

# 📥 **4. Incoming Payload (Cloud → Local)**

Cloud LLM responds with:

```json
{
  "masked_response": "<masked_final_answer>"
}
```

### Requirements:

* Must contain **placeholders exactly as received**.
* Must not generate new placeholder types.
* Must not include personal data.
* Must respect all rules defined in the prompt.

---

# 📌 **5. HTTP Communication Details**

### **Method:**

`POST`

### **Content-Type:**

`application/json`

### **Endpoints Options:**

* Custom server (FastAPI, Flask, Node.js)
* Cloud function endpoint
* OpenAI API
* Gemini API
* Ollama cloud endpoint
* Your own server on Render/Hetzner/EC2

### **Min Required Headers:**

```
Content-Type: application/json
Authorization: Bearer <API_KEY>   (optional depending on service)
```

---

# 🔒 **6. Privacy & Security Rules**

1. Local device **must never send unmasked content**.
2. Cloud LLM must not receive:

   * Real names
   * Real amounts
   * Real dates
   * Reference IDs
   * Actual messages
3. Even if the cloud is compromised, only placeholders leak.
4. All business logic stays local:

   * Entity extraction
   * Placeholder replacement
   * Arithmetic
   * Storage

---

# 🧠 **7. Error Handling Rules**

Local device must handle:

### **A. Cloud API timeout**

Fallback:

```
"Unable to reach the assistant right now. Try again."
```

### **B. Cloud returns empty or invalid response**

Fallback:

```
"Something went wrong generating the answer."
```

### **C. Cloud removes placeholders (unexpected)**

Local solution:

* Reject the response
* Retry with stricter instructions
* Log the issue

### **D. Cloud invents new placeholders**

Reject:

```
"Invalid placeholder modification detected."
```

---

# 📦 **8. Example End-to-End Local → Cloud → Local Cycle**

### **Local → Cloud**

```json
{
  "query": "How much did I pay?",
  "messages": [
    "Payment of Rs. #amount_1 to #receiver_1.",
    "Invoice due: Rs. #amount_2."
  ],
  "prompt_template": "You are a reasoning assistant... (full template)"
}
```

### **Cloud Response → Local**

```json
{
  "masked_response": "You paid #amount_1 and #amount_2. Total = (#amount_1 + #amount_2)."
}
```

### **Local Reconstruction**

Final answer →

```
"You paid 150 and 2000. Total = 2150."
```

---

# 🏁 **9. Summary**

This interface specification allows you to:

* Communicate safely with a cloud LLM
* Guarantee privacy
* Keep processing lightweight on device
* Maintain consistent structure
* Avoid hallucinations
* Scale easily
