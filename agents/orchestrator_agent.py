from agents.expense_logger_agent import Expense_Logger_Agent
from agents.expense_summary_agent import Expense_Summary_Agent
from agents.budget_Info_Agent import Budget_Info_Agent


class Orchestrator_Agent:
    def __init__(self):
        self.expense_logger_agent = Expense_Logger_Agent()
        self.expense_summary_agent = Expense_Summary_Agent()
        self.budget_info_agent = Budget_Info_Agent()

    def handle(self, plan: dict) -> dict:
        tool_names = plan["tool_name"]
        tool_args_list = plan["tool_args"]

        print(f"Types of tool_name : {type(tool_names)}")
        print(f"Types of tool_args : {tool_args_list}")

        contexts = []
        for tool_name, tool_args in zip(tool_names, tool_args_list):
            if tool_name == "log_expense":
                context = self.expense_logger_agent.execute(tool_args)
                print(f"context for  {tool_name}  this query is : {context}")
            elif tool_name == "get_spending_summary":
                context = self.expense_summary_agent.execute(tool_args)
                print(f"context for  {tool_name}  this query is : {context}")
            elif tool_name == "check_budget_status":
                context = self.budget_info_agent.execute(tool_args)
               
                print(f"context for {tool_name} this query is : {context}")
            else:
                raise ValueError(f"Unknown tool_name: {tool_name}")
            contexts.append(context)

        print(f"context for this query is : {context}")
           

        return {"context": contexts, "query": plan["query"]}
