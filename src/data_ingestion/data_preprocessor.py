import json
import os
import sys
from src.logging.logger import logging
from src.exception.exception import Project_Exception

from src.entity.config_entity import DataIngistionConfig, ProjectPipelineConfig


class DataIngestion:
    """
    Handles reading local SMS and Email files and saving them 
    in structured form under artifacts/data_ingestion/processed/.
    """
    def __init__(self, data_ingestion_config :DataIngistionConfig ):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise Project_Exception(e,sys)
        

    # def __init__(self, raw_data_dir="data/sample_messages", processed_dir="artifacts/data_ingestion/processed"):
    #     self.raw_data_dir = raw_data_dir
    #     self.processed_dir = processed_dir
    #     os.makedirs(self.processed_dir, exist_ok=True)
    #     logging.info("DataIngestion initialized successfully.")

    def read_sms_messages(self):
        """
        Reads sms.json from local directory and saves as sms_data.json
        """
        try:
            sms_path = self.data_ingestion_config.sms_dir
            output_path = os.path.join(self.data_ingestion_config.processed_data_dir, "sms_data.json")

            if not os.path.exists(sms_path):
                logging.warning("sms.json not found. Skipping SMS ingestion.")
                return None

            with open(sms_path, "r", encoding="utf-8") as f:
                sms_data = json.load(f).get("messages", [])

            formatted_sms = []
            for msg in sms_data:
                formatted_sms.append({
                    "type": "sms",
                    "sender": msg.get("sender"),
                    "subject": None,
                    "body": msg.get("text"),
                    "timestamp": msg.get("timestamp")
                })

            # Save processed SMS
            
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(formatted_sms, f, indent=4)

            logging.info(f"Processed and saved {len(formatted_sms)} SMS messages to {output_path}")
            return output_path

        except Exception as e:
            raise Project_Exception(e, sys)

    def read_email_messages(self):
        """
        Reads emails.json from local directory and saves as email_data.json
        """
        try:
            email_path = os.path.join(self.data_ingestion_config.email_dir)
            output_path = os.path.join(self.data_ingestion_config.processed_data_dir, "email_data.json")

            if not os.path.exists(email_path):
                logging.warning("emails.json not found. Skipping email ingestion.")
                return None

            with open(email_path, "r", encoding="utf-8") as f:
                email_data = json.load(f).get("emails", [])

            formatted_emails = []
            for mail in email_data:
                formatted_emails.append({
                    "type": "email",
                    "sender": mail.get("from"),
                    "subject": mail.get("subject"),
                    "body": mail.get("body"),
                    "timestamp": mail.get("date")
                })

            # Save processed emails

            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(formatted_emails, f, indent=4)

            logging.info(f"Processed and saved {len(formatted_emails)} email messages to {output_path}")
            return output_path

        except Exception as e:
            raise Project_Exception(e, sys)


if __name__ == "__main__":
    project_pipeline_config = ProjectPipelineConfig()
    data_ingestion_config_obj = DataIngistionConfig(project_pipeline_config)
    data_ingestion_obj = DataIngestion(data_ingestion_config_obj)
    data_ingestion_obj.read_sms_messages()
    data_ingestion_obj.read_email_messages()
