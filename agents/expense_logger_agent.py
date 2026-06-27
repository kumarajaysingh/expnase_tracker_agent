from mcp_tools.tool_manager import TOOL_REGISTRY


class Expense_Logger_Agent:
    def execute(self, tool_args: dict) -> str:
        """ Here it is calling the real function"""
        return TOOL_REGISTRY["log_expense"](**tool_args)
