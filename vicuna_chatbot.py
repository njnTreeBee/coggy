# vicuna_chatbot.py
import spacy

class VicunaChatbot:
    def __init__(self, model_name):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.global_workspace = set()  # Use a set to store unique elements
        self.nlp = spacy.load("en_core_web_sm")  # Load the spaCy language model

    def _update_global_workspace(self, input_text):
        # Process the input text using spaCy
        doc = self.nlp(input_text)

        # Extract keywords by selecting nouns and proper nouns
        keywords = [token.text for token in doc if token.pos_ in ["NOUN", "PROPN"]]

        # Extract named entities
        named_entities = [ent.text for ent in doc.ents]

        # Extract semantic relationships by iterating through tokens
        relationships = []
        for token in doc:
            if token.dep_ in ("nsubj", "dobj"):
                subj = token.text
                verb = token.head.text
                obj = " ".join([t.text for t in token.head.children if t.dep_ == ("dobj" if token.dep_ == "nsubj" else "nsubj")])
                if obj:
                    relationships.append((subj, verb, obj))

        # Update the global workspace with the new elements
        self.global_workspace.update(keywords)
        self.global_workspace.update(named_entities)
        self.global_workspace.update(relationships)

    def generate_response(self, input_text):
        self._update_global_workspace(input_text)  # Update the global workspace before generating a response

        input_ids = self.tokenizer.encode(input_text, return_tensors="pt")
        output = self.model.generate(input_ids, max_length=100, num_return_sequences=1)
        response = self.tokenizer.decode(output[0], skip_special_tokens=True)
        return response
