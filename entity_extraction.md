

# 📄 **Entity Extraction Rules (v1)**

This document defines how the system extracts real values (amounts, names, dates, etc.) from messages before masking them into unique placeholders.

All extraction is done **locally**, and no personal data is ever sent to the cloud.

---

# 🔢 **1. Entity Types to Extract**

The system will extract the following entities from each message:

* **Amount** (money values)
* **Receiver / Person names**
* **Payment App / Source**
* **Reference ID**
* **Date**
* **Time**
* **Miscellaneous nouns (movie, invoice, ticket, etc.)**

---

# 🧠 **2. Extraction Method for Each Entity Type**

Below are the rules that define *how* each entity is detected.

---

## **2.1 Amount Extraction**

Detect currency amounts in forms such as:

* `Rs. 150`
* `₹150`
* `INR 400`
* `Rs.150/-`
* `150 Rs`

**Regex Pattern (concept):**

```
(Rs\.?\s*\d+|₹\s*\d+|INR\s*\d+|\d+\s*Rs)
```

---

## **2.2 Receiver / Person Extraction**

Detect person names appearing after keywords:

* `to <name>`
* `from <name>`
* `paid to <name>`
* `sent to <name>`

**Pattern Examples:**

```
to ([A-Za-z]+)
from ([A-Za-z]+)
```

**Note:**
Later, spaCy NER can be added for robust name detection.

---

## **2.3 Payment App / Source Extraction**

Detect known payment apps such as:

* Google Pay
* PhonePe
* Paytm
* Amazon Pay
* BHIM
* Debit/Credit Card

**Keyword-Based Detection:**
Match exact keywords.

---

## **2.4 Reference ID Extraction**

Detect alphanumeric transaction IDs:

Examples:

* `Ref ID: GP281105`
* `UPI Ref: 1234567890`
* `Txn ID: ABCD1234`

**Pattern (concept):**

```
(Ref ID|UPI Ref|Txn ID)[:\s]+([A-Za-z0-9]+)
```

---

## **2.5 Date Extraction**

Common date formats:

* `28 Oct`
* `2025-11-03`
* `03/11/2025`
* `November 3`

**Patterns:**

* DD MMM
* YYYY-MM-DD
* DD/MM/YYYY

---

## **2.6 Time Extraction**

Detect times in formats:

* `7 PM`
* `19:30`
* `9:45 am`

**Pattern examples:**

```
(\d{1,2}:\d{2}\s*(AM|PM)?)|(\d{1,2}\s*(AM|PM))
```

---

## **2.7 Miscellaneous Nouns**

Non-sensitive nouns that describe context:

* movie
* ticket
* invoice
* subscription
* show

Extracted via simple keyword matching.

---

# 📦 **3. Output Format for Extraction**

For each message, extraction produces a dictionary:

```
{
  "<placeholder>": "<original_value>"
}
```

Example:

```json
{
  "#amount_1": "150",
  "#receiver_1": "Ravi",
  "#source_1": "PhonePe",
  "#refid_1": "GP12345"
}
```

Each message gets a unique index ( `_1`, `_2`, `_3` ).

---

# ⚠️ **4. Missing Entity Rules**

If an entity is missing:

* Do **not** create a placeholder for that field
* Mask only what exists
* Ensure the masked message stays readable

**Example:**
If no receiver name is present:

Original:

```
"Payment of Rs. 200 was successful."
```

Masked:

```
"Payment of Rs. #amount_1 was successful."
```

Entity map:

```json
{
  "#amount_1": "200"
}
```

---

# 🧪 **5. Complete Example Extraction**

### Original Message

```
"Payment of Rs. 350 to Aman via Paytm was successful. Ref ID: TXN9988"
```

### Message Index

`1`

### Extracted Entities

```
#amount_1 → 350
#receiver_1 → Aman
#source_1 → Paytm
#refid_1 → TXN9988
```

### Masked Message

```
"Payment of Rs. #amount_1 to #receiver_1 via #source_1 was successful. Ref ID: #refid_1."
```

---

# 🎯 Purpose of This Step

This extraction specification ensures:

* Accurate masking
* Correct placeholder assignment
* Perfect privacy
* Predictable behavior for the cloud LLM
* Seamless final reconstruction


