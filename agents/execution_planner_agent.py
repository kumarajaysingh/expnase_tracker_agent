import json

from openai_client import MODEL, get_client
from mcp_tools.tool_manager import TOOL_SCHEMAS
from prompts.tool_calling_prompt import tools_calling_prompt
from conversation_history.history import get_history, get_history_size

class Execution_Planner_Agent:

    def build_messages(self, query: str, history: list) -> list:
        messages = [{"role": "system", "content": tools_calling_prompt}]

        for entry in history:
            messages.append({"role": entry["role_user"], "content": entry["user_query"]})
            messages.append({"role": entry["role_ai"], "content": entry["ai_response"]})

        messages.append({
            "role": "user",
            "content": query,
        })
        return messages
    
    def plan(self, query: str) -> dict:
        client = get_client()
        con_history = get_history()
        messages = self.build_messages(query, con_history)
        print(f"History message=======>> : {get_history_size}")
        print(f"User query in executer planner : {query}")
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOL_SCHEMAS,
            tool_choice="auto",
        )

        message = response.choices[0].message
        print(f"message from 1st llm call: {message}")
        tool_calls = message.tool_calls

        if not tool_calls:
            return {"tool_name": None, "tool_args": {}, "query": query}

        #tool_call = tool_calls[0]
        #tool_name = tool_call.function.name
        tool_name = []
        tool_args = []
        for tool in tool_calls:
            tool_name.append(tool.function.name)
            tool_args.append(json.loads(tool.function.arguments or "{}"))
        #tool_args = json.loads(tool_call.function.arguments or "{}")




        return {"tool_name": tool_name, "tool_args": tool_args, "query": query}
