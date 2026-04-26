from config.settings import SYSTEM_PROMPT, REPORT_TRIGGER_WORDS

class PromptBuilder:
    def __init__(self, system_prompt=SYSTEM_PROMPT):
        self.system_prompt = system_prompt

    def _is_report_query(self, query):
        query_lower = query.lower()
        return any(word in query_lower for word in REPORT_TRIGGER_WORDS)

    def _prioritize_report(self, chunks):
        report_chunks = [c for c in chunks if c.get("source") == "report.txt"]
        other_chunks  = [c for c in chunks if c.get("source") != "report.txt"]
        return report_chunks + other_chunks

    def build(self, query, retrieved_chunks, history):
        if self._is_report_query(query):
            retrieved_chunks = self._prioritize_report(retrieved_chunks)

        context_lines = []
        for item in retrieved_chunks:
            source = item.get("source", "unknown")
            chunk  = item.get("chunk", "")
            context_lines.append(f"[Source: {source}]\n{chunk}")
        context_block = "\n\n".join(context_lines)

        is_report = self._is_report_query(query)
        if is_report:
            answer_format = (
                "Structure your answer as:\n"
                "**Findings:** (bullet points from the report)\n"
                "**Diagnosis:** (one line)\n"
                "**What it means:** (plain language explanation)\n"
                "**Recommended next steps:** (brief)\n"
            )
        else:
            answer_format = (
                "Structure your answer as:\n"
                "**Definition:** (one line)\n"
                "**Key facts:** (3-5 full sentence bullet points covering causes, types, symptoms, or important characteristics — NOT single words)\n"
                "**In simple terms:** (plain language summary in 2-3 sentences)\n"
            )

        system_message = (
            f"{self.system_prompt}\n\n"
            "Use the context below to answer the user's question.\n"
            "If the answer is not in the context, say you don't know.\n"
            "Always be concise and medically accurate.\n\n"
            f"{answer_format}\n"
            "=== CONTEXT ===\n"
            f"{context_block}\n"
            "==============="
        )

        messages = [{"role": "system", "content": system_message}]
        messages.extend(history)
        messages.append({"role": "user", "content": query})
        return messages
