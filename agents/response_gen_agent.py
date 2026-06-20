from openai_client import MODEL, get_client

SYSTEM_PROMPT = (
    "You are a helpful expense-tracking assistant. You are given the user's "
    "original question and context returned from an internal tool call (e.g. a "
    "logged expense confirmation or a spending summary). Use ONLY the "
    "information in the context to answer the user's question in clear, "
    "natural language. Do not invent numbers or details not present in the "
    "context. If the context indicates an error, apologize and explain "
    "briefly what went wrong."
)


class Response_Gen_Agent:
    def generate(self, query: str, context: str) -> str:
        client = get_client()
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": f"User question: {query}\n\nTool context: {context}",
                },
            ],
        )
        return response.choices[0].message.content
