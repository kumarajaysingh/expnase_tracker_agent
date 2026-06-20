from tool_manager import TOOL_REGISTRY


class Expense_Summary_Agent:
    def execute(self, tool_args: dict) -> str:
        return TOOL_REGISTRY["get_spending_summary"](**tool_args)
