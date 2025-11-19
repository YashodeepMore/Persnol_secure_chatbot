Here is a clean, ready-to-paste **Markdown Placeholder Masking Schema Document**.
Copy → Paste into your markdown file.

---

# 📄 **Unique Placeholder Masking Schema (v1)**

This document defines the masking rules used in the hybrid AI message assistant.
All personal data is replaced with unique placeholders before sending text to the cloud LLM.

---

## 🔢 **1. Indexing Rule**

* Each retrieved message is assigned an index:

  * Message 1 → `_1`
  * Message 2 → `_2`
  * Message 3 → `_3`
* All placeholders inside the same message use the **same index**.

Example:
If message 2 has amount and receiver → `#amount_2`, `#receiver_2`.

---

## 🔤 **2. Placeholder Naming Format**

Use the following template:

```
#entitytype_i
```

Where:

* `entitytype` = category of the information
* `i` = message index

---

## 🧩 **3. Supported Entity Types**

| Entity Type          | Placeholder Format | Example       |
| -------------------- | ------------------ | ------------- |
| Amount / Money       | `#amount_i`        | `#amount_1`   |
| Person / Receiver    | `#receiver_i`      | `#receiver_2` |
| Payment App / Source | `#source_i`        | `#source_1`   |
| Reference ID         | `#refid_i`         | `#refid_1`    |
| Date                 | `#date_i`          | `#date_3`     |
| Noun / Item / Misc   | `#noun_i`          | `#noun_3`     |
| Time                 | `#time_i`          | `#time_2`     |

You can add new types later when needed.

---

## 🎯 **4. Masking Rules**

1. **Every detected entity in a message must be replaced with a placeholder.**
2. **Never reuse the same placeholder across different messages.**
3. **Never use a placeholder without an index.**
   (❌ `#amount` → ✔️ `#amount_1`)
4. **Do not introduce new placeholder types inside the LLM.**
5. **Cloud LLM must NOT modify placeholders.**
6. **Cloud LLM computes totals or summarization using placeholders**
   (e.g., `#amount_1 + #amount_2`).

---

## 📦 **5. Data Structure for Each Message**

Each message must produce **two outputs**:

### **A. Masked Text**

Example:

```
"Payment of Rs. #amount_1 to #receiver_1 via #source_1 was successful."
```

### **B. Entity Map**

Example:

```json
{
  "#amount_1": "150",
  "#receiver_1": "Ravi",
  "#source_1": "Google Pay",
  "#refid_1": "GP281105"
}
```

---

## 🧪 **6. Complete Example**

### **Original Message**

```
"Payment of Rs. 150 to Ravi via Google Pay was successful. Ref ID: GP281105."
```

### **Assigned Index**

Message index = 1

### **Masked Message**

```
"Payment of Rs. #amount_1 to #receiver_1 via #source_1 was successful. Ref ID: #refid_1."
```

### **Entity Map**

```json
{
  "#amount_1": "150",
  "#receiver_1": "Ravi",
  "#source_1": "Google Pay",
  "#refid_1": "GP281105"
}
```

---

## 🧠 **7. Purpose of This Schema**

This masking system allows:

* Privacy-preserving RAG
* Safe cloud LLM usage
* Multi-message reasoning (summation, comparison, etc.)
* Local reconstruction of final answers

---

If you want, I can also generate a **prompt template document** in the same clean markdown format.
