import os

import requests
from dotenv import load_dotenv

load_dotenv()

EXPENSE_API_BASE_URL = os.environ.get("EXPENSE_API_BASE_URL", "http://localhost:8000")

REQUEST_TIMEOUT_SECONDS = 10


def log_expense(amount: float, category: str, description: str = "", date: str = "") -> str:
    payload = {
        "amount": amount,
        "category": category,
        "description": description,
        "date": date,
    }
    try:
        response = requests.post(
            f"{EXPENSE_API_BASE_URL}/api/expense",
            json=payload,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        return f"status_code={response.status_code} body={response.text}"
    except requests.RequestException as exc:
        return f"error calling log_expense tool: {exc}"


def get_spending_summary(category: str = "", start_date: str = "", end_date: str = "") -> str:
    params = {}
    if category:
        params["category"] = category
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date

    try:
        response = requests.get(
            f"{EXPENSE_API_BASE_URL}/api/expense/summary",
            params=params,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        return f"status_code={response.status_code} body={response.text}"
    except requests.RequestException as exc:
        return f"error calling get_spending_summary tool: {exc}"
    

def check_budget_status(category: str = "") -> dict:
    params = {}
    if category:
        params["category"] = category

    try:
        response = requests.get(
            f"{EXPENSE_API_BASE_URL}/api/budget/info",
            params=params,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        return f"status_code={response.status_code} body={response}"
    except requests.RequestException as exc:
        return f"error calling get_spending_summary tool: {exc}"


TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "log_expense",
            "description": "Log a new expense with an amount, category, optional description and date.",
            "parameters": {
                "type": "object",
                "properties": {
                    "amount": {
                        "type": "number",
                        "description": "The amount spent.",
                    },
                    "category": {
                        "type": "string",
                        "description": "The expense category, e.g. Groceries, Travel.",
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional free-text description of the expense.",
                    },
                    "date": {
                        "type": "string",
                        "description": "Date of the expense in DD-MM-YYYY format.",
                    },
                },
                "required": ["amount", "category"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_spending_summary",
            "description": "Get a summary of spending, filtered by category and/or date range.",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Optional category to filter the summary by.",
                    },
                    "start_date": {
                        "type": "string",
                        "description": "Optional start date in DD-MM-YYYY format.",
                    },
                    "end_date": {
                        "type": "string",
                        "description": "Optional end date in DD-MM-YYYY format.",
                    },
                },
                "required": ["category",],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "check_budget_status",
            "description": "Get a status of Budget, filtered by category.",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Required category to filter the summary by.",
                    },
                   
                },
                "required": ["category",],
            },
        },
    },
]

TOOL_REGISTRY = {
    "log_expense": log_expense,
    "get_spending_summary": get_spending_summary,
    "check_budget_status": check_budget_status
}
