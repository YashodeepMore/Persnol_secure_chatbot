

# 📄 **Placeholder Re-Fill Rules (Local Reconstruction) — v1**

This document specifies how the system reconstructs the final natural answer **locally** by replacing placeholders with real entity values.

This step happens **after** receiving the masked response from the cloud LLM.

---

# 🎯 **1. Purpose**

To convert a cloud LLM response like:

```
"You paid #amount_1 and #amount_2. Total = (#amount_1 + #amount_2)."
```

Into:

```
"You paid 150 and 2000. Total = 2150."
```

All done **locally**, ensuring privacy.

---

# 🧱 **2. Inputs Required for Placeholder Re-Fill**

The re-fill module receives:

### **A. Cloud LLM Response**

Masked text containing placeholders.

Example:

```
"You paid #amount_1 to #receiver_1."
```

### **B. Entity Maps (From Extraction Stage)**

Data structure storing real values:

```json
{
  "#amount_1": "150",
  "#receiver_1": "Ravi"
}
```

You will have **one entity map per message**, then merged.

---

# 🔁 **3. Re-Fill Process**

### **Step 1 — Merge all entity dictionaries**

Example:

```json
{
  "#amount_1": "150",
  "#receiver_1": "Ravi",
  "#amount_2": "2000",
  "#receiver_2": "Aman"
}
```

### **Step 2 — Replace placeholders in the LLM response**

For each placeholder key:

* Search for `#placeholder`
* Replace with the corresponding real value

### **Step 3 — Compute any expressions if present**

Cloud LLM may return something like:

```
Total = (#amount_1 + #amount_2)
```

Your local system should:

* Detect `(#amount_1 + #amount_2)`
* Replace each placeholder value
* Compute the numeric result (150+2000=2150)
* Update the sentence accordingly

---

# 🧠 **4. Rules for Correct and Safe Reconstruction**

1. **Never send real values back to cloud LLM.**
   Reconstruction happens offline only.

2. **Fill only the placeholders that exist in the entity map.**

3. **If a placeholder is missing in the map:**

   * Leave it unchanged
   * Or replace with `"unknown"` (your choice)

4. **If the message involves arithmetic:**

   * Only compute operations with numeric values
   * Never assume missing values
   * If values missing → show partial total or say cannot compute

5. **Final output must contain ZERO placeholders.**

---

# 📦 **5. Example: Complete Reconstruction**

### **Masked LLM Output**

```
"You paid #amount_1 for dinner and #amount_2 for materials. Total = (#amount_1 + #amount_2)."
```

### **Entity Map**

```json
{
  "#amount_1": "150",
  "#amount_2": "2000"
}
```

### **Local Reconstruction Steps**

Replace placeholders:

```
"You paid 150 for dinner and 2000 for materials. Total = (150 + 2000)."
```

Compute arithmetic:

```
"You paid 150 for dinner and 2000 for materials. Total = 2150."
```

---

# 🚫 **6. If Cloud LLM Uses Same Placeholder Twice**

Example:

```
"You have two payments of #amount_1."
```

Entity map:

```
#amount_1 → 300
```

Final output:

```
"You have two payments of 300."
```

If cloud LLM says total cannot be computed → keep that logic.

---

# 🧪 **7. Example: Missing Data Handling**

Masked LLM output:

```
"Payment processed to #receiver_1 on #date_1."
```

Entity map missing `#date_1`:

```
#receiver_1 → "Aman"
```

You can choose either:

### Option A — Keep placeholder

```
"Payment processed to Aman on #date_1."
```

### Option B — Replace with "unknown"

```
"Payment processed to Aman on unknown."
```

(Your choice — document your preference.)

---

# 🏁 **8. Summary**

This placeholder re-fill system ensures:

* 100% privacy
* Zero data leakage
* Correct reasoning
* Clean final answers
* Cloud LLM stays blind to personal data