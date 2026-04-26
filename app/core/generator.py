from groq import Groq
from config.settings import GROQ_API_KEY, GROQ_MODEL

class ResponseGenerator:
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)
        self.model  = GROQ_MODEL

    def generate(self, messages):
        groq_messages  = []
        system_content = None
        for msg in messages:
            if msg["role"] == "system":
                system_content = msg["content"]
            else:
                groq_messages.append(msg)
        if system_content:
            groq_messages.insert(0, {"role": "system", "content": system_content})
        response = self.client.chat.completions.create(
            model=self.model,
            messages=groq_messages,
            temperature=0.3
        )
        return response.choices[0].message.content
