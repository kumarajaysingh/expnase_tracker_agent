from agents.expense_logger_agent import Expense_Logger_Agent
from agents.expense_summary_agent import Expense_Summary_Agent
from agents.budget_Info_Agent import Budget_Info_Agent


class Orchestrator_Agent:
    def __init__(self):
        self.expense_logger_agent = Expense_Logger_Agent()
        self.expense_summary_agent = Expense_Summary_Agent()
        self.budget_info_agent = Budget_Info_Agent()

    def handle(self, plan: dict) -> dict:
        tool_name = plan["tool_name"]
        tool_args = plan["tool_args"]

        if tool_name == "log_expense":
            context = self.expense_logger_agent.execute(tool_args)
        elif tool_name == "get_spending_summary":
            context = self.expense_summary_agent.execute(tool_args)
        elif tool_name == "check_budget_status":
            context = self.budget_info_agent.execute(tool_args)
        else:
            raise ValueError(f"Unknown tool_name: {tool_name}")

        return {"context": context, "query": plan["query"]}
