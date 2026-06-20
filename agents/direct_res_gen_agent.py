from openai_client import MODEL, get_client

SYSTEM_PROMPT = (
    "You are a helpful, general-purpose assistant for an expense-tracking "
    "app. Answer the user's question directly and concisely."
)


class Direct_Res_Gen_Agent:
    def generate(self, query: str) -> str:
        client = get_client()
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": query},
            ],
        )
        return response.choices[0].message.content
