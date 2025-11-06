import json
import numpy as np
import faiss
import os
import sys

from src.exception.exception import Project_Exception
from src.logging.logger import logging
from src.entity.artifact_entity import DataIngestionArtifact

# embedding_service/vector_store.py

class VectorStore:
    try:
        def __init__(self, data_ingestion_artifact:DataIngestionArtifact):
            """
            VectorStore handles loading processed messages (SMS & Emails),
            storing their embeddings, and enabling semantic search with FAISS.
            """

            self.base_dir = data_ingestion_artifact.processed_data_dir
            self.index_dir = data_ingestion_artifact.artifact_dir
            self.email_path = data_ingestion_artifact.email_path
            self.sms_path = data_ingestion_artifact.sms_path
            os.makedirs(self.index_dir, exist_ok=True)

            self.index = None
            self.messages = []          # list of combined message texts
            self.metadata = []          # stores sender, date, etc.
            self.embeddings = None
    except Exception as e:
        raise Project_Exception(e,sys)

    # ----------------------------------------------------------------
    # 1️⃣ Load and preprocess SMS + Email messages
    # ----------------------------------------------------------------
    def load_messages(self):
        try:
            # sms_path = os.path.join(self.base_dir, "sms.json")
            # email_path = os.path.join(self.base_dir, "email.json")
            sms_path = self.sms_path
            email_path = self.email_path

            all_texts = []
            meta = []

            # --- Load SMS messages ---
            if os.path.exists(sms_path):
                with open(sms_path, "r", encoding="utf-8") as f:
                    sms_data = json.load(f)
                    for msg in sms_data:
                        # Construct a searchable text form
                        text = f"SMS from {msg.get('sender', 'Unknown')}: {msg.get('text', '')}"
                        all_texts.append(text.strip())

                        meta.append({
                            "source": "sms",
                            "sender": msg.get("sender"),
                            "timestamp": msg.get("timestamp"),
                            "type": msg.get("type"),
                            "details": msg.get("details", {})
                        })

            # --- Load Emails ---
            if os.path.exists(email_path):
                with open(email_path, "r", encoding="utf-8") as f:
                    email_data = json.load(f)
                    for mail in email_data:
                        # Combine subject and body
                        subject = mail.get("subject", "")
                        body = mail.get("body", "")
                        text = f"Email from {mail.get('from', 'Unknown')} about '{subject}': {body}"
                        all_texts.append(text.strip())

                        meta.append({
                            "source": "email",
                            "from": mail.get("from"),
                            "date": mail.get("date"),
                            "type": mail.get("type"),
                            "details": mail.get("details", {})
                        })

            self.messages = all_texts
            self.metadata = meta

            logging.info(f"[INFO] Loaded {len(all_texts)} total messages (SMS + Emails).")
            return all_texts, meta
        except Exception as e:
            raise Project_Exception(e,sys)
    # ----------------------------------------------------------------
    # 2️⃣ Save embeddings and metadata
    # ----------------------------------------------------------------


    def save_data(self, embeddings):
        try:
            os.makedirs(self.index_dir, exist_ok=True)
            np.save(os.path.join(self.index_dir, "embeddings.npy"), embeddings)
            with open(os.path.join(self.index_dir, "messages.json"), "w", encoding="utf-8") as f:
                json.dump(self.messages, f, ensure_ascii=False, indent=2)
            with open(os.path.join(self.index_dir, "metadata.json"), "w", encoding="utf-8") as f:
                json.dump(self.metadata, f, ensure_ascii=False, indent=2)
            logging.info("[INFO] Saved embeddings, messages, and metadata.")
        except Exception as e:
            raise Project_Exception(e,sys)
    # ----------------------------------------------------------------
    # 3️⃣ Build and store FAISS index
    # ----------------------------------------------------------------
    def build_index(self, embeddings):
        try:
            dim = embeddings.shape[1]
            self.index = faiss.IndexFlatL2(dim)
            self.index.add(embeddings)
            faiss.write_index(self.index, os.path.join(self.index_dir, "index.faiss"))
            logging.info("[INFO] FAISS index built and saved.")
        except Exception as e:
            raise Project_Exception(e,sys)
    # ----------------------------------------------------------------
    # 4️⃣ Load index + embeddings
    # ----------------------------------------------------------------
    def load_index(self):
        try:
            self.index = faiss.read_index(os.path.join(self.index_dir, "index.faiss"))
            self.embeddings = np.load(os.path.join(self.index_dir, "embeddings.npy"))
            with open(os.path.join(self.index_dir, "messages.json"), "r", encoding="utf-8") as f:
                self.messages = json.load(f)
            with open(os.path.join(self.index_dir, "metadata.json"), "r", encoding="utf-8") as f:
                self.metadata = json.load(f)
            logging.info("[INFO] Loaded FAISS index and message data.")
        except Exception as e:
            raise Project_Exception(e,sys)

    # ----------------------------------------------------------------
    # 5️⃣ Search function (semantic search)
    # ----------------------------------------------------------------
    def search(self, query_embedding, top_k=5):
        try:
            if self.index is None:
                self.load_index()
            distances, indices = self.index.search(np.array(query_embedding), top_k)

            results = []
            for rank, (idx, dist) in enumerate(zip(indices[0], distances[0])):
                result = {
                    "rank": rank + 1,
                    "text": self.messages[idx],
                    "distance": float(dist),
                    "metadata": self.metadata[idx]
                }
                results.append(result)
            return results
        except Exception as e:
            raise Project_Exception(e,sys)
