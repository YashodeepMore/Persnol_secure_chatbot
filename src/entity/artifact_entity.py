from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    sms_path:str
    email_path:str
    processed_data_dir:str
    artifact_dir:str

