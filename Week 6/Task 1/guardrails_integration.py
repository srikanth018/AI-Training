from sentence_transformers import SentenceTransformer, util

class ConcertGuardrails:
    def __init__(self, threshold=0.60):
        """
        Initialize guardrails with sentence transformers
        
        Args:
            threshold: Similarity threshold for intent matching (default: 0.60)
        """
        self.model = SentenceTransformer("all-mpnet-base-v2")
        self.threshold = threshold
        
        # Define allowed intents/topics
        self.allowed_intents = [
            "book concert ticket",
            "find concert details",
            "venue info for a concert",
            "search for concerts",
            "check venue availability",
            "get ticket prices",
            "artist information",
            "upcoming concerts",
            "concert dates",
            "live music events",
            "concert booking",
            "ticket availability",
            "Hi , Hello , Hey",
        ]
        
        # Pre-compute embeddings for allowed intents
        self.allowed_embeddings = self.model.encode(self.allowed_intents)

    def is_in_scope(self, user_query):
        """
        Check if user query is within allowed scope
        
        Args:
            user_query: User's input query
            
        Returns:
            bool: True if query is in scope, False otherwise
        """
        query_emb = self.model.encode(user_query)
        scores = util.cos_sim(query_emb, self.allowed_embeddings)
        max_score = scores.max().item()
        
        print(f"[GUARDRAILS] Similarity score: {max_score:.3f} (threshold: {self.threshold})")
        return max_score >= self.threshold

    def run(self, user_input: str) -> str | None:
        """
        Run guardrails check on user input
        
        Args:
            user_input: User's input query
            
        Returns:
            str | None: Error message if out of scope, None if in scope
        """
        print("[GUARDRAILS] Running guardrails check...")
        
        if self.is_in_scope(user_input):
            print("[GUARDRAILS] Query passed guardrails")
            return None
        else:
            print("[GUARDRAILS] Blocked out-of-scope query")
            return "I'm a concert booking assistant and can only help with concert-related queries."


def create_guardrails(threshold: float = 0.60) -> ConcertGuardrails:
    """
    Factory function to create guardrails instance
    
    Args:
        threshold: Similarity threshold for intent matching (default: 0.60)
        
    Returns:
        ConcertGuardrails instance
    """
    return ConcertGuardrails(threshold=threshold)
