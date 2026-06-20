import json

from openai_client import MODEL, get_client
from tool_manager import TOOL_SCHEMAS


class Execution_Planner_Agent:
    def plan(self, query: str) -> dict:
        client = get_client()
        print(f"User query in executer planner : {query}")
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": query}],
            tools=TOOL_SCHEMAS,
            tool_choice="auto",
        )

        message = response.choices[0].message
        print(f"message from 1st llm call: {message}")
        tool_calls = message.tool_calls

        if not tool_calls:
            return {"tool_name": None, "tool_args": {}, "query": query}

        tool_call = tool_calls[0]
        tool_name = tool_call.function.name
        tool_args = json.loads(tool_call.function.arguments or "{}")

        return {"tool_name": tool_name, "tool_args": tool_args, "query": query}
