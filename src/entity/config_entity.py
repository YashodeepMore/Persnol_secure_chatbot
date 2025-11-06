import os
from datetime import datetime

from src.constants import message_pipeline

print(message_pipeline.PIPELINE_NAME)
print(message_pipeline.ARTIFACT_DIR_NAME)

class ProjectPipelineConfig:
    def __init__(self, timestamp = datetime.now()):
        timestamp = timestamp.strftime("%d_%m_%Y_%H_%M_%S")
        self.pipeline_name = message_pipeline.PIPELINE_NAME
        self.artifact_name = message_pipeline.ARTIFACT_DIR_NAME
        self.artifact_dir = os.path.join(self.artifact_name,timestamp)
        self.raw_data_dir = os.path.join("data",message_pipeline.RAW_DATA_DIR_NAME)
        self.timestamp: str=timestamp


class DataIngistionConfig:
    def __init__(self, project_pipeline_config: ProjectPipelineConfig):
        self.artifact_dir = project_pipeline_config.artifact_dir
        self.data_ingestion_dir : str=os.path.join(
            project_pipeline_config.artifact_dir, message_pipeline.DATA_INGESTION_DIR_NAME
        )
        
        self.processed_data_dir :str = os.path.join(
            project_pipeline_config.artifact_dir,message_pipeline.DATA_INGESTION_DIR_NAME,message_pipeline.PROCESSED_DATA_DIR_NAME
        )

        self.raw_data_dir :str = os.path.join(project_pipeline_config.raw_data_dir,"sample_messages")
        self.sms_dir : str = os.path.join(self.raw_data_dir,message_pipeline.RAW_SMS_DIR_NAME)
        self.email_dir : str = os.path.join(self.raw_data_dir,message_pipeline.RAW_EMAIL_DIR_NAME)
        

class DataPreprocessingConfig:
    def __init__(self,project_pipeline_config: ProjectPipelineConfig):
        self.preprocessed_data_dir :str = os.path.join(
            project_pipeline_config.artifact_dir,message_pipeline.DATA_INGESTION_DIR_NAME,message_pipeline.PROCESSED_DATA_DIR_NAME
        )

        self.raw_data_dir :str = os.path.join(project_pipeline_config.raw_data_dir,"sample_messages")
        self.sms_dir : str = os.path.join(self.raw_data_dir,message_pipeline.RAW_SMS_DIR_NAME)
        self.email_dir : str = os.path.join(self.raw_data_dir,message_pipeline.RAW_EMAIL_DIR_NAME)