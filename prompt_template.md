
# 📄 **Cloud LLM Prompt Template (v1)**

This document defines the standardized prompt format used to communicate with the cloud LLM.
It ensures:

* Predictable responses
* No hallucinations
* Strict placeholder preservation
* Privacy compliance

---

# 🎯 **1. Prompt Purpose**

The cloud LLM receives:

* The **user’s query**
* A list of **clean masked RAG messages**

The LLM must:

* Understand the query
* Use only masked messages
* Never replace placeholders
* Generate a short, natural masked answer
* Allow multi-message reasoning (e.g., summing placeholders)

---

# 🧩 **2. Prompt Structure**

The final prompt sent to the LLM should always follow this structure:

```
You are a reasoning assistant for a privacy-safe RAG system.

IMPORTANT RULES:
- The messages contain placeholders like #amount_i, #receiver_i, #date_i.
- NEVER modify, replace, remove, or invent placeholders.
- ALWAYS keep placeholders EXACTLY as they appear.
- NEVER hallucinate real numbers, names, or dates.
- Use only the masked messages provided.
- Perform reasoning using placeholders (e.g., #amount_1 + #amount_2).
- Ignore irrelevant messages or messages that do not answer the query.
- If information is missing or placeholders repeat, explain the limitation.

USER QUERY:
"<user_query>"

RETRIEVED MESSAGES:
1. "<masked_message_1>"
2. "<masked_message_2>"
3. "<masked_message_3>"

TASK:
Based on the masked messages, generate a short, natural answer that:
- Uses ONLY placeholders
- Follows all rules above
- Is accurate, concise, and helpful
```

---

# 🧠 **3. Example Prompt**

```
You are a reasoning assistant for a privacy-safe RAG system.

IMPORTANT RULES:
- Never replace placeholders like #amount_1 or #receiver_2.
- Never create new placeholders.
- Never hallucinate real details.
- If amounts use same placeholder, you cannot compute total.

USER QUERY:
"I paid some people, can you calculate total amount?"

RETRIEVED MESSAGES:
1. "Payment of Rs. #amount_1 to #receiver_1 for dinner."
2. "Invoice due: Rs. #amount_2 for raw materials."
3. "Movie tickets confirmed. No payment."

TASK:
Create a short answer using placeholders only.
```

---

# 📌 **4. Expected LLM Response Examples**

### **Case 1: Different placeholders**

```
You have two payments: #amount_1 and #amount_2.
Total = (#amount_1 + #amount_2).
```

### **Case 2: Same placeholder repeated**

```
Two messages show payments, both using #amount_1.
Total cannot be calculated because placeholders are identical.
```

### **Case 3: Irrelevant messages**

```
Only the first two messages represent payments with #amount_1 and #amount_2.
The third message is unrelated.
```

---

# 🔐 **5. Privacy Requirements**

The LLM must:

* Never see real data
* Never output real data
* Never modify placeholders
* Never add or remove placeholders

Placeholders ensure **complete privacy**.

---

# 📦 **6. When to Update This Document**

You should update this template when:

* You add new placeholder types
* You refine system reasoning
* You add special-case instructions (e.g., refunds, reminders, dates)

---

# 🏁 **7. Summary**

This prompt template ensures:

* Stability
* Predictability
* Privacy
* High-quality reasoning
* No hallucinations


