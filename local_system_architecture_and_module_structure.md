
This document outlines **what modules this local system will have**,
**what each module is responsible for**,
and **how they interact**.

This is the foundation before writing any actual code.

---

# 📄 **Local System Architecture & Module Structure (v1)**

This document defines the components of the **local (on-device) system** in the hybrid privacy-safe RAG assistant.

The architecture is modular to keep the system maintainable, testable, and secure.

---

# 🧱 **1. Purpose**

To clearly define:

* What modules the local system will have
* What each module does
* How data flows between them
* What responsibilities stay local (privacy-critical)

This ensures all future coding is structured and consistent.

---

# 🧩 **2. Core Local Modules**

The system will contain the following local modules:

---

## **2.1 `data_loader.py`**

**Responsibility:**

* Load SMS and email JSON files
* Normalize message format
* Provide messages to the embedding generator

**Outputs:**

* A clean list of raw messages

---

## **2.2 `embedding_engine.py`**

**Responsibility:**

* Use MiniLM (local embedding model)
* Generate embeddings
* Maintain FAISS index
* Allow dynamic message addition

**Outputs:**

* Top-K similar messages for a query
* Message indices for downstream modules

---

## **2.3 `entity_extractor.py`**

**Responsibility:**

* Apply Entity Extraction Rules
* Detect amount, receiver, date, etc.
* Assign unique placeholder IDs (`_1`, `_2`, `_3`)
* Produce:

  * Masked message
  * Entity map

**Outputs:**

```json
{
  "masked_message": "...",
  "entities": {
    "#amount_1": "150",
    "#receiver_1": "Ravi"
  }
}
```

---

## **2.4 `rag_cleaner.py`**

**Responsibility:**

* Clean raw FAISS results
* Remove logs, timestamps, metadata
* Format into the final clean RAG message format

**Outputs:**

```
1. "Payment of Rs. #amount_1 to #receiver_1."
2. "Invoice due: Rs. #amount_2."
```

---

## **2.5 `prompt_builder.py`**

**Responsibility:**

* Insert:

  * User query
  * Clean masked messages
  * Cloud LLM rules
* Create the final prompt for cloud usage
* Ensure strict placeholder rules

**Output:**
A full text prompt to send to cloud LLM.

---

## **2.6 `cloud_interface.py`**

**Responsibility:**

* Send prompt to cloud LLM
* Receive masked response
* Handle timeouts, validation, errors

**Output:**

```
{
  "masked_response": "<...>"
}
```

---

## **2.7 `placeholder_refill.py`**

**Responsibility:**

* Merge entity maps
* Replace placeholders with real values
* Evaluate arithmetic (if present)
* Produce final natural answer

**Output:**
Clean natural response text.

---

## **2.8 `main.py`**

**Responsibility:**

* Orchestrate full pipeline
* Steps:

  1. User query → embeddings → top-K results
  2. Extract + mask entities
  3. Clean RAG messages
  4. Build cloud prompt
  5. Call cloud LLM
  6. Refill placeholders
  7. Return final answer

---

# 🔄 **3. Local Data Flow**

```
User Query
 → embedding_engine (FAISS search)
 → entity_extractor (masking)
 → rag_cleaner (clean messages)
 → prompt_builder (final prompt)
 → cloud_interface (LLM call)
 → placeholder_refill (local reconstruction)
 → Final Answer
```

---

# 🔐 **4. Privacy Responsibilities**

The following MUST stay local:

* Raw SMS and email content
* Entity extraction
* Entity maps
* Placeholder re-fill
* Final user answer
* Embeddings
* FAISS index

Only **masked messages + query** go to the cloud.

---

# 📦 **5. Benefits of This Architecture**

* Modular → easy to maintain and improve
* Secure → all sensitive tasks local
* Scalable → change cloud model anytime
* Testable → each module can be tested independently
* Future-proof → can add NER, KG, caching, etc.

---

# 🏁 **6. Summary**

This architecture defines:

* All local modules
* Their responsibilities
* The order in which they operate
* Privacy boundaries
* System behavior
