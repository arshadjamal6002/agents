# api_server.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from orchestrator_agent import handle_user_input, AGENTS, AGENT_CONFIGS
import uvicorn

app = FastAPI(title="Multi-Agent GenAI API")

class InstructRequest(BaseModel):
    input: str | dict

@app.post("/instruct")
def instruct_route(req: InstructRequest):
    try:
        result = handle_user_input(req.input)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/agent/{agent_id}")
def agent_route(agent_id: str, req: InstructRequest):
    if agent_id not in AGENTS:
        raise HTTPException(status_code=404, detail="Agent not found")
    try:
        result = AGENTS[agent_id].run(req.input)
        return {
            "agent": agent_id,
            "output": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/agents")
def list_agents():
    return [
        {
            "name": a["name"],
            "description": a.get("description", ""),
            "required_inputs": a.get("required_inputs", []) # <-- ADD THIS LINE
        }
        for a in AGENT_CONFIGS
    ]
if __name__ == "__main__":
    uvicorn.run("api_server:app", host="0.0.0.0", port=8000, reload=True)

# uvicorn api_server:app --reload

# POST http://localhost:8000/instruct
# {
#   "input": "Can you explain this code to me?"
# }
