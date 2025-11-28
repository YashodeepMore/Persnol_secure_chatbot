import os
import sys

from src.logging.logger import logging
from src.exception.exception import Project_Exception

from src.entity.artifact_entity import DataIngestionArtifact
from src.entity.config_entity import ProjectPipelineConfig,DataIngistionConfig
from src.data_ingestion.data_preprocessor import DataIngestion
from src.embedding_service.embedding_generator import  EmbeddingGenerator
from src.embedding_service.vector_store import VectorStore
from src.query_engine.entity_extractor import EntityExtractor
from tests.test_api_class import CloudLLM

if __name__=="__main__":
    try:
        project_pipeline_config = ProjectPipelineConfig()
        data_ingestion_config = DataIngistionConfig(project_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_dataingestion()

        store = VectorStore(data_ingestion_artifact)
        messages, metadata = store.load_messages()

        # Step 2: Generate embeddings
        embedder = EmbeddingGenerator()
        embeddings = embedder.generate_embeddings(messages)

        # Step 3: Save + build index
        store.save_data(embeddings)
        store.build_index(embeddings)

        # Step 4: Run search
        query = input("Enter your search query: ")
        query_emb = embedder.generate_embeddings([query])
        results = store.search(query_emb, top_k=3)

        

        logging.info("\nTop Matches:\n")
        for r in results:
            logging.info(f"{r['rank']}. {r['text']}")
            logging.info(f"   Type: {r['metadata']['type']}, Distance: {r['distance']:.3f}\n")

        new_message = {
            "sender": "Google Pay",
            "timestamp": "2025-11-07T10:05:00",
            "text": "Payment of Rs. 250 to Rajesh for dinner was successful. Ref ID: GP281105.",
            "type": "transaction",
            "details": {"amount": 250, "action": "debited"}
        }

        store.add_new_message(new_message, embedder)
        query = input("Enter your search query: ")
        query_emb = embedder.generate_embeddings([query])
        results = store.search(query_emb, top_k=3)

        logging.info("\nTop Matches:\n")
        for r in results:
            logging.info(f"{r['rank']}. {r['text']}")
            logging.info(f"   Type: {r['metadata']['type']}, Distance: {r['distance']:.3f}\n")

        messages = [mes['text'] for mes in results]
        result = EntityExtractor.extract_entities_from_messages(messages)

        print("\n--- MASKED MESSAGES ---")
        for m in result["masked_messages"]:
            print(m)

        print("\n--- PLACEHOLDER MAP ---")
        print(result["placeholder_map"])


        llm = CloudLLM()

        prompt = f"""
        You are a natural-language reasoning assistant for a RAG system.

        IMPORTANT RULES:
        - The text contains masked entities like #amount, #receiver, #date.
        - These placeholders MUST remain EXACTLY as they appear.
        - NEVER replace, modify, create, or remove placeholders.
        - Never hallucinate real names, numbers, dates, or apps.
        - Only summarize or compute using the placeholders given.
        - Ignore messages that do NOT contain #amount if question is about payments.
        - If total cannot be calculated because placeholders are the same, say so.

        USER QUERY:
        {query}

        RETRIEVED MESSAGES:
        {messages}

        TASK:
        - Identify which messages represent payments.
        - Use only the placeholders to calculate.
        - If multiple different #amount placeholders exist, express total as (#amount + #amount).
        - If the same placeholder repeats, say: 
        "Both payments use the placeholder #amount, so the total cannot be calculated."

        Give final answer in 1–2 sentences.
        """

        response = llm.send_prompt(prompt)

        print("LLM Response:", response)

    except Exception as e:
        raise Project_Exception(e,sys)