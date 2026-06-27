from openai_client import MODEL, get_client
from conversation_history.history import get_history, get_history_size, add_history

SYSTEM_PROMPT1 = (
    "You are a helpful expense-tracking assistant. You are given the user's "
    "original question and context returned from an internal tool call (e.g. a "
    "logged expense confirmation or a spending summary). Use ONLY the "
    "information in the context to answer the user's question in clear, "
    "natural language. Do not invent numbers or details not present in the "
    "context. If the context indicates an error, apologize and explain "
    "briefly what went wrong."
)

SYSTEM_PROMPT = """You are a helpful personal finance assistant. You help users track their 
expenses, manage budgets, and understand their spending patterns.

Key behaviors:
- When users mention spending money, log it as an expense using the log_expense tool
- When users ask about spending, use get_spending_summary to get accurate data
- When users want to set budgets, use set_budget
- When users ask about budget status, use check_budget_status
- Always confirm actions with the user in a friendly, concise way
- Use ₹ (INR) as the currency symbol
- If a date isn't mentioned, assume today
- If a category isn't clear, make your best guess and mention it

Today's date is: {today}
"""


class Response_Gen_Agent:

    def add_conversation_history(self, user_query: str, ai_response: str) -> None:
        add_history({
            "role_user": "user",
            "user_query": user_query,
            "role_ai": "assistant",
            "ai_response": ai_response,
        })

    def build_messages(self, query: str, context: str, history: list) -> list:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]

        for entry in history:
            messages.append({"role": entry["role_user"], "content": entry["user_query"]})
            messages.append({"role": entry["role_ai"], "content": entry["ai_response"]})

        messages.append({
            "role": "user",
            "content": f"User question: {query}\n\nTool context: {context}",
        })
        return messages

    def generate(self, query: str, context: str) -> str:
        client = get_client()
        con_history = get_history()
        messages = self.build_messages(query, context, con_history)
        print(f"History message in 2nd LLM=======>> : {messages}")

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
        )
        answer = response.choices[0].message.content
        self.add_conversation_history(query, answer)
        print(f"History message in 2nd LLM=======>> : {get_history_size()}")
        return answer
    

