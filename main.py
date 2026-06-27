from fastapi import FastAPI
from pydantic import BaseModel

from agents.direct_res_gen_agent import Direct_Res_Gen_Agent
from agents.execution_planner_agent import Execution_Planner_Agent
from agents.orchestrator_agent import Orchestrator_Agent
from agents.response_gen_agent import Response_Gen_Agent

app = FastAPI()

execution_planner_agent = Execution_Planner_Agent()
orchestrator_agent = Orchestrator_Agent()
response_gen_agent = Response_Gen_Agent()
direct_res_gen_agent = Direct_Res_Gen_Agent()


class ChatRequest(BaseModel):
    query: str


class ChatResponse(BaseModel):
    response: str


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    plan = execution_planner_agent.plan(request.query)

    if not plan["tool_name"]:
        answer = direct_res_gen_agent.generate(request.query)
    else:
        result = orchestrator_agent.handle(plan)
        answer = response_gen_agent.generate(result["query"], result["context"])

    return ChatResponse(response=answer)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8002)
