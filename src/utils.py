import logging
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PIIMasker:
    def __init__(self):
        try:
            self.analyzer = AnalyzerEngine()
            self.anonymizer = AnonymizerEngine()
            logger.info("Presidio Analyzer and Anonymizer initialized successfully.")
        except Exception as e:
            logger.error(f"Error initializing Presidio: {e}")
            raise

    def mask_text(self, text: str) -> str:
        """
        Analyzes the text for PII and masks it.
        Target entities: PHONE_NUMBER, EMAIL_ADDRESS, PERSON, US_SSN, CREDIT_CARD
        """
        if not text:
            return ""

        # Define entities to look for
        entities = ["PHONE_NUMBER", "EMAIL_ADDRESS", "PERSON", "US_SSN", "CREDIT_CARD"]
        
        # Analyze
        results = self.analyzer.analyze(text=text, entities=entities, language='en')
        
        # Anonymize
        # We replace with the entity type, e.g., <PHONE_NUMBER>
        anonymized_result = self.anonymizer.anonymize(
            text=text,
            analyzer_results=results,
            operators={
                "PHONE_NUMBER": OperatorConfig("replace", {"new_value": "<PHONE_NUMBER>"}),
                "EMAIL_ADDRESS": OperatorConfig("replace", {"new_value": "<EMAIL_ADDRESS>"}),
                "PERSON": OperatorConfig("replace", {"new_value": "<PERSON>"}),
                "US_SSN": OperatorConfig("replace", {"new_value": "<SSN>"}),
                "CREDIT_CARD": OperatorConfig("replace", {"new_value": "<CREDIT_CARD>"}),
            }
        )
        
        return anonymized_result.text

if __name__ == "__main__":
    # Simple test
    masker = PIIMasker()
    sample_text = "Call John Doe at 555-123-4567 or email him at john.doe@example.com."
    print(f"Original: {sample_text}")
    print(f"Masked: {masker.mask_text(sample_text)}")
