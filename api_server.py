# api_server.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from orchestrator_agent import handle_user_input, AGENTS, AGENT_CONFIGS
import uvicorn
import os
import json

app = FastAPI(title="Multi-Agent GenAI API")

class InstructRequest(BaseModel):
    input: str | dict

# --- Helper to load config from disk ---
def get_agent_config_from_file(agent_name):
    """
    Reads the config.json for a specific agent to get its required inputs.
    """
    try:
        config_path = f"agents/{agent_name}/config.json"
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                return json.load(f)
    except Exception:
        pass
    return {}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Multi-Agent GenAI API! Use /docs for documentation."}

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
    """
    Returns a list of agents with their descriptions and REQUIRED INPUTS
    loaded dynamically from their config.json files.
    """
    agent_list = []
    for a in AGENT_CONFIGS:
        # Load the real config from disk to ensure we have 'required_inputs'
        file_config = get_agent_config_from_file(a["name"])
        
        # Merge the basic config with the file config
        agent_info = {
            "name": a["name"],
            "description": file_config.get("description", a.get("description", "")),
            # This is the critical part that was missing:
            "required_inputs": file_config.get("required_inputs", [])
        }
        agent_list.append(agent_info)
    return agent_list

if __name__ == "__main__":
    uvicorn.run("api_server:app", host="0.0.0.0", port=8000, reload=True)