# embedding_service/embedding_generator.py

import os
import numpy as np
import sys
from sentence_transformers import SentenceTransformer

from src.exception.exception import Project_Exception
from src.logging.logger import logging

class EmbeddingGenerator:
    try:

        def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
            logging.info("[INFO] Loading embedding model...")
            logging.info(f"loading {model_name} ")
            self.model = SentenceTransformer(model_name)

        def generate_embeddings(self, texts):
            """Convert list of texts to embeddings"""
            logging.info(f"[INFO] Generating embeddings for {len(texts)} texts...")
            embeddings = self.model.encode(texts, show_progress_bar=True)
            return np.array(embeddings)
        
    except Exception as e:
        raise Project_Exception(e,sys)
