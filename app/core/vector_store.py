import os
import pickle
import numpy as np
import faiss
from config.settings import CACHE_FILE


class VectorStore:
    def __init__(self):
        self.chunks  = []   # list of {"chunk": str, "source": str}
        self.index   = None # FAISS index (built after first add)
        self.dim     = None # embedding dimension

    # Add chunks + embeddings

    def add(self, chunks, embeddings, source="unknown"):
        vectors = np.array(embeddings, dtype=np.float32)

        # Normalize for cosine similarity
        faiss.normalize_L2(vectors)

        # Build index on first call
        if self.index is None:
            self.dim   = vectors.shape[1]
            self.index = faiss.IndexFlatIP(self.dim)  # Inner Product = cosine after normalize

        self.index.add(vectors)

        for chunk in chunks:
            self.chunks.append({"chunk": chunk, "source": source})

    # Persistent cache

    def save(self, path=CACHE_FILE):
        cache = {
            "chunks": self.chunks,
            "dim":    self.dim,
            "index":  faiss.serialize_index(self.index) if self.index else None
        }
        with open(path, "wb") as f:
            pickle.dump(cache, f)
        print(f"[Cache] Saved {len(self.chunks)} chunks to {path}")

    def load(self, path=CACHE_FILE):
        if not os.path.isfile(path):
            return False
        with open(path, "rb") as f:
            cache = pickle.load(f)
        self.chunks = cache["chunks"]
        self.dim    = cache["dim"]
        if cache["index"] is not None:
            self.index = faiss.deserialize_index(cache["index"])
        print(f"[Cache] Loaded {len(self.chunks)} chunks from {path}")
        return True

    def is_cache_valid(self, docs_folder, report_file, cache_path=CACHE_FILE):
        """Return True if cache is newer than all source files."""
        if not os.path.isfile(cache_path):
            return False
        cache_mtime = os.path.getmtime(cache_path)

        if os.path.isfile(report_file):
            if os.path.getmtime(report_file) > cache_mtime:
                return False

        if os.path.isdir(docs_folder):
            for fname in os.listdir(docs_folder):
                fpath = os.path.join(docs_folder, fname)
                if os.path.getmtime(fpath) > cache_mtime:
                    return False

        return True

    # Search with optional forced sources

    def search(self, query_embedding, top_k=5, force_sources=None):
        if not self.chunks or self.index is None:
            return []

        # Separate forced chunks first
        forced_results  = []
        forced_indices  = set()

        if force_sources:
            for i, entry in enumerate(self.chunks):
                if entry["source"] in force_sources:
                    forced_indices.add(i)
                    forced_results.append({
                        "chunk":  entry["chunk"],
                        "source": entry["source"],
                        "score":  0.0   # will be filled below
                    })

        # FAISS search across all chunks
        query_vec = np.array([query_embedding], dtype=np.float32)
        faiss.normalize_L2(query_vec)

        search_k = top_k + len(forced_indices)  # fetch extra to fill remaining slots
        scores, indices = self.index.search(query_vec, min(search_k, len(self.chunks)))

        # Fill scores for forced chunks
        score_map = {int(idx): float(score) for idx, score in zip(indices[0], scores[0])}
        for r in forced_results:
            i = next((j for j, c in enumerate(self.chunks)
                      if c["chunk"] == r["chunk"] and c["source"] == r["source"]), None)
            if i is not None and i in score_map:
                r["score"] = round(score_map[i], 4)

        # Fill remaining slots from FAISS results (skip forced)
        remaining_slots = top_k - len(forced_results)
        normal_results  = []

        for idx, score in zip(indices[0], scores[0]):
            idx = int(idx)
            if idx == -1:
                continue
            if idx in forced_indices:
                continue
            normal_results.append({
                "chunk":  self.chunks[idx]["chunk"],
                "source": self.chunks[idx]["source"],
                "score":  round(float(score), 4)
            })
            if len(normal_results) >= remaining_slots:
                break

        return forced_results + normal_results

    def clear(self):
        self.chunks = []
        self.index  = None
        self.dim    = None
