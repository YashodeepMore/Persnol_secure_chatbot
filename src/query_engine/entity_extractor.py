import re
from typing import Dict, List


class EntityExtractor:

    # -----------------------------
    # REGEX PATTERNS
    # -----------------------------
    AMOUNT_REGEX = re.compile(r'(?:Rs\.?|₹)\s?(\d[\d,]*)')
    DATE_REGEX = re.compile(
        r'\b(\d{1,2}\s?(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s?\d{0,4})\b',
        re.IGNORECASE,
    )
    REFID_REGEX = re.compile(r'(?:Ref(?:erence)?(?:\sID)?:?\s?)([A-Za-z0-9]+)')
    NAME_REGEX = re.compile(r'\bto\s([A-Z][a-zA-Z]+)\b')
    CAPITAL_WORD_REGEX = re.compile(r'\b([A-Z][a-zA-Z]+)\b')

    # ------------------------------------------------------
    # INDIVIDUAL EXTRACTION FUNCTIONS
    # ------------------------------------------------------

    @staticmethod
    def extract_amount(msg: str) -> str:
        match = EntityExtractor.AMOUNT_REGEX.search(msg)
        if match:
            return match.group(1).replace(",", "")
        return None

    @staticmethod
    def extract_date(msg: str) -> str:
        match = EntityExtractor.DATE_REGEX.search(msg)
        if match:
            return match.group(1)
        return None

    @staticmethod
    def extract_refid(msg: str) -> str:
        match = EntityExtractor.REFID_REGEX.search(msg)
        if match:
            return match.group(1)
        return None

    @staticmethod
    def extract_receiver(msg: str) -> str:
        match = EntityExtractor.NAME_REGEX.search(msg)
        if match:
            return match.group(1)
        return None

    @staticmethod
    def extract_source(msg: str) -> str:
        # Choose first capital word: SMS, Email, Google, BookMyShow etc.
        matches = EntityExtractor.CAPITAL_WORD_REGEX.findall(msg)
        if matches:
            return matches[0]
        return None

    # ------------------------------------------------------
    # ASSIGN PLACEHOLDERS BASED ON MESSAGE INDEX
    # ------------------------------------------------------
    @staticmethod
    def assign_placeholders(entities: Dict, idx: int) -> Dict:
        placeholder_map = {}
        for key, value in entities.items():
            ph_key = f"{key}_{idx}"
            placeholder_map[ph_key] = value
        return placeholder_map

    # ------------------------------------------------------
    # CREATE MASKED MESSAGE
    # ------------------------------------------------------
    @staticmethod
    def mask_message(msg: str, placeholders: Dict) -> str:
        masked = msg
        for key, value in placeholders.items():
            placeholder = f"#{key}"

            # Replace clean number: 45000
            masked = masked.replace(str(value), placeholder)

            # Replace comma version: 45,000
            if value.isdigit():
                comma_value = "{:,}".format(int(value))
                masked = masked.replace(comma_value, placeholder)

        return masked

    # ------------------------------------------------------
    # MAIN PIPELINE FUNCTION (ORCHESTRATOR)
    # ------------------------------------------------------
    @staticmethod
    def extract_entities_from_messages(messages: List[str]) -> Dict:
        all_placeholders = {}
        masked_messages = []

        for idx, msg in enumerate(messages, start=1):

            # Extract all entity types
            entities = {
                "amount": EntityExtractor.extract_amount(msg),
                "date": EntityExtractor.extract_date(msg),
                "refid": EntityExtractor.extract_refid(msg),
                "receiver": EntityExtractor.extract_receiver(msg),
                "source": EntityExtractor.extract_source(msg),
            }

            # Remove None entries
            entities = {k: v for k, v in entities.items() if v is not None}

            # Add suffix (_1, _2, …)
            placeholders = EntityExtractor.assign_placeholders(entities, idx)

            # Add to global map
            all_placeholders.update(placeholders)

            # Create masked message
            masked = EntityExtractor.mask_message(msg, placeholders)
            masked_messages.append(masked)

        return {
            "masked_messages": masked_messages,
            "placeholder_map": all_placeholders
        }


# from entity_extractor import EntityExtractor
if __name__=="__main__":

    messages = [
        "SMS from Google Pay: Payment of Rs. 250 to Rajesh for dinner was successful. Ref ID: GP281105.",
        "Email from Unknown: Attached is invoice. Total amount due: Rs. 45,000. Kindly process payment by 15 November 2025.",
        "SMS from BookMyShow: Your tickets for the movie 'Fighter' are confirmed. Ref: BMS5599"
    ]

    result = EntityExtractor.extract_entities_from_messages(messages)

    print("\n--- MASKED MESSAGES ---")
    for m in result["masked_messages"]:
        print(m)

    print("\n--- PLACEHOLDER MAP ---")
    print(result["placeholder_map"])
