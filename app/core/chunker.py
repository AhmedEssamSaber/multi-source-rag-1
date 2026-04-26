from config.settings import CHUNK_SIZE, CHUNK_OVERLAP

class TextChunker:
    def chunk(self, text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start += chunk_size - overlap
        return chunks
