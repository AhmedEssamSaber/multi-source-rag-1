import cohere
from config.settings import COHERE_API_KEY

class EmbeddingModel:
    def __init__(self):
        self.co = cohere.Client(COHERE_API_KEY)

    def embed(self, texts, input_type="search_document"):
        if not texts:
            raise ValueError("texts list is empty")
        response = self.co.embed(
            texts=texts,
            model="embed-english-v3.0",
            input_type=input_type
        )
        return response.embeddings

    def rerank(self, query, chunks, top_n=5):
        """Rerank retrieved chunks using Cohere reranker."""
        if not chunks:
            return []
        docs = [c["chunk"] for c in chunks]
        response = self.co.rerank(
            query=query,
            documents=docs,
            model="rerank-english-v3.0",
            top_n=top_n
        )
        reranked = []
        for result in response.results:
            original = chunks[result.index]
            reranked.append({
                "chunk":  original["chunk"],
                "source": original["source"],
                "score":  round(result.relevance_score, 4)
            })
        return reranked
