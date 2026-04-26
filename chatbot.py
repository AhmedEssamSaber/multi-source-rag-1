import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from app.core.chunker       import TextChunker
from app.core.embedder      import EmbeddingModel
from app.core.vector_store  import VectorStore
from app.core.memory        import ConversationMemory
from app.core.prompt_builder import PromptBuilder
from app.core.generator     import ResponseGenerator
from config.settings        import (
    DOCS_FOLDER, REPORT_FILE,
    RETRIEVAL_TOP_K, RERANK_TOP_N, CONFIDENCE_THRESHOLD
)


class Chatbot:
    def __init__(self):
        self.chunker   = TextChunker()
        self.embedder  = EmbeddingModel()
        self.store     = VectorStore()
        self.memory    = ConversationMemory()
        self.builder   = PromptBuilder()
        self.generator = ResponseGenerator()
        self._load_all_sources()

    def _load_all_sources(self):
        if self.store.is_cache_valid(DOCS_FOLDER, REPORT_FILE):
            self.store.load()
            return
        print("[Cache] Rebuilding index...")
        self._load_docs_folder(DOCS_FOLDER)
        self._load_report(REPORT_FILE)
        self.store.save()

    def _load_docs_folder(self, folder):
        if not os.path.isdir(folder):
            print(f"[Warning] docs folder '{folder}' not found.")
            return
        for filename in sorted(os.listdir(folder)):
            if filename.endswith(".txt"):
                self._index_file(os.path.join(folder, filename), source=filename)

    def _load_report(self, filepath):
        if not os.path.isfile(filepath):
            print(f"[Warning] report file '{filepath}' not found.")
            return
        self._index_file(filepath, source="report.txt")

    def _index_file(self, filepath, source):
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
        chunks = self.chunker.chunk(text)
        if not chunks:
            return
        embeddings = self.embedder.embed(chunks, input_type="search_document")
        self.store.add(chunks, embeddings, source=source)
        print(f"[Indexed] {source} → {len(chunks)} chunks")

    def chat(self, user_query):
        query_embedding = self.embedder.embed([user_query], input_type="search_query")[0]
        force    = ["report.txt"] if self.builder._is_report_query(user_query) else None
        retrieved = self.store.search(query_embedding, top_k=RETRIEVAL_TOP_K, force_sources=force)
        retrieved = self.embedder.rerank(user_query, retrieved, top_n=RERANK_TOP_N)
        confidence = self._confidence(retrieved)
        messages   = self.builder.build(
            query=user_query,
            retrieved_chunks=retrieved,
            history=self.memory.get_history()
        )
        answer = self.generator.generate(messages)
        self.memory.add("user", user_query)
        self.memory.add("assistant", answer)
        return answer, retrieved, confidence

    def _confidence(self, retrieved):
        if not retrieved:
            return 0.0
        return round(sum(r["score"] for r in retrieved) / len(retrieved), 4)


if __name__ == "__main__":
    bot = Chatbot()
    print("Chatbot ready. Type 'quit' to exit.\n")
    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit"):
            break
        answer, sources, confidence = bot.chat(user_input)
        print(f"\nAssistant: {answer}")
        label = "⚠️ Low" if confidence < CONFIDENCE_THRESHOLD else "✅"
        print(f"\n{label} Confidence: {confidence:.4f}")
        print("\n[Sources used]")
        for s in sources:
            print(f"  - {s['source']} (score: {s['score']:.4f})")
        print()
