import spacy
import json

def extract_capabilities(documentation):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(documentation)
    
    capabilities = {}
    for token in doc:
        if token.pos_ == 'NOUN':
            if token.text not in capabilities:
                capabilities[token.text] = token.sent.text

    return capabilities

def store_ai_capabilities(ai_id, capabilities):
    # Assuming you have a function to store the extracted capabilities in your blockchain platform
    # ...

def main():
    # Load AI documentation (e.g., from a file, an API, or any other source)
    ai_id = 'AI-12345'
    documentation = """
    This AI system supports multiple languages, including English, Spanish, and Chinese. 
    It is built using the OpenAI GPT-4 model and offers various NLP tasks such as sentiment analysis, text summarization, and named entity recognition.
    """

    # Extract capabilities
    capabilities = extract_capabilities(documentation)
    print(f"Extracted capabilities: {json.dumps(capabilities, indent=2)}")

    # Store extracted capabilities in the blockchain platform
    store_ai_capabilities(ai_id, capabilities)

if __name__ == "__main__":
    main()
