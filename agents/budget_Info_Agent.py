from mcp_tools.tool_manager import TOOL_REGISTRY

class Budget_Info_Agent:
    def execute(self, tool_args: dict) -> str:
            """ Here it is calling the real function"""
            return TOOL_REGISTRY["check_budget_status"](**tool_args)
