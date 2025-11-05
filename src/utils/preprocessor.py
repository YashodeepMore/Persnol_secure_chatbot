from src.logging.logger import logging
from src.exception.exception import Project_Exception
import sys

import re
from datetime import datetime
from typing import Dict



def preprocess_text(text: str) -> str:

    try:
        """
        Cleans and normalizes message or email text for analysis.
        Steps:
        - Lowercase the text
        - Remove extra spaces and special characters
        - Normalize money formats (e.g., Rs. → Rs)
        - Remove multiple spaces
        """
        if not text:
            return ""
        
        # 1. Lowercase
        text = text.lower()
        
        # 2. Normalize "Rs.", "₹" etc.
        text = re.sub(r'rs\.?', 'rs', text)
        text = text.replace('₹', 'rs')
        
        # 3. Remove unnecessary punctuation (keep numbers, %, ., and : for timestamps)
        text = re.sub(r'[^a-z0-9\s\.\:\%]', ' ', text)
        
        # 4. Collapse multiple spaces
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    except Exception as e:
        raise Project_Exception(e,sys)



def analyze_sms(message: Dict) -> Dict:
    
    try:
        """
        Analyzes an SMS and extracts useful structured info.
        Returns dictionary with type, amount, sender, and key details.
        """
        text = message.get("body", "")
        sender = message.get("sender", "Unknown")
        timestamp = message.get("timestamp", "")
        
        clean_text = preprocess_text(text)
        info = {
            "sender": sender,
            "timestamp": timestamp,
            "text": text,
            "type": "general",
            "details": {}
        }

        # Detect transaction SMS
        match_amount = re.search(r'rs[\s\.]?\s?([0-9,]+)', clean_text)
        if "debited" in clean_text or "credited" in clean_text:
            info["type"] = "transaction"
            if match_amount:
                amount = match_amount.group(1).replace(",", "")
                info["details"]["amount"] = float(amount)
            if "debited" in clean_text:
                info["details"]["action"] = "debited"
            elif "credited" in clean_text:
                info["details"]["action"] = "credited"

        # Detect order/delivery SMS
        elif "order" in clean_text or "delivered" in clean_text:
            info["type"] = "order_update"
            order_match = re.search(r'order\s*#?(\d+)', clean_text)
            if order_match:
                info["details"]["order_id"] = order_match.group(1)
            delivery_match = re.search(r'deliver(?:ed|y)?\s*(?:by|on)?\s*([a-z0-9\s:]+)', clean_text)
            if delivery_match:
                info["details"]["delivery_time"] = delivery_match.group(1).strip()

        # Detect reminder
        elif "remind" in clean_text or "due" in clean_text:
            info["type"] = "reminder"

        return info
    except Exception as e:
        raise Project_Exception(e,sys)



def analyze_email(email: Dict) -> Dict:
        
    try: 
        """
        Analyzes an email and extracts structured information.
        Returns dictionary with type, extracted details, and metadata.
        """
        sender = email.get("from", "Unknown")
        subject = email.get("subject", "")
        body = email.get("body", "")
        date = email.get("timestamp", "")

        clean_text = preprocess_text(subject + " " + body)
        info = {
            "from": sender,
            "subject": subject,
            "date": date,
            "body": body,
            "type": "general",
            "details": {}
        }

        # --- Detect meeting reminders ---
        if "meeting" in clean_text or "schedule" in clean_text or "review" in clean_text:
            info["type"] = "meeting"
            time_match = re.search(r'(\d{1,2}\s?(?:am|pm|a\.m\.|p\.m\.))', clean_text)
            day_match = re.search(r'(monday|tuesday|wednesday|thursday|friday|saturday|sunday|tomorrow)', clean_text)
            if time_match:
                info["details"]["time"] = time_match.group(1)
            if day_match:
                info["details"]["day"] = day_match.group(1)

        # --- Detect offer / internship / onboarding ---
        elif "offer" in clean_text or "internship" in clean_text or "selected" in clean_text:
            info["type"] = "offer"
            join_match = re.search(r'onboarding\s+on\s+([0-9]{1,2}(?:st|nd|rd|th)?\s+\w+)', clean_text)
            if join_match:
                info["details"]["onboarding_date"] = join_match.group(1)

        # --- Detect confirmation / action needed ---
        elif "confirm" in clean_text or "response" in clean_text:
            info["type"] = "confirmation_request"

        # --- Detect reminder or alert ---
        elif "remind" in clean_text or "due" in clean_text:
            info["type"] = "reminder"

        return info
    except Exception as e:
        raise Project_Exception(e,sys)
